"""
Extrator Oficial de Itens Sem Giro e Aging de Estoque
GW Wireless - Performance Operacional Logístico
Conecta no ERP S7 (Relatorios.VW_Logistica_Detalhada) para extrair o histórico real de vendas
e cruza com o inventário físico auditado das 6 filiais (dashboard_full_data.json).
"""

import os
import json
import time
from datetime import datetime, date
import pymssql
from dotenv import load_dotenv

load_dotenv('c:/Users/renan.alves/.gemini/Projetos/Bancos/.env')

ERP_TO_FILIAL = {
    1: 12, 8: 12,       # Matriz (Lojas 1 e 8)
    6: 9, 90: 9,        # Goiânia (Lojas 6 e 90)
    9: 8, 91: 8,        # Brasília (Lojas 9 e 91)
    10: 11, 11: 11,     # Palmas (Lojas 10 e 11)
    7: 10, 92: 10,      # Marabá (Lojas 7 e 92)
    14: 7               # São Luís (Loja 14)
}

def estimate_unit_price(desc, sku_code):
    desc_upper = (desc or "").upper()
    if any(k in desc_upper for k in ['MA5800', 'OLT HUAWEI', 'MA5608T', 'MAQUINA DE FUSAO', 'OTDR', 'BATERIA ESTACIONARIA', 'AIR FIBER', 'AF-5XHD', 'EDGE ROUTER', 'SWITCH 24', 'SWITCH 48', 'CCR1036', 'CCR1009', 'CCR2004']):
        return 450.00
    elif any(k in desc_upper for k in ['CABO OPTICO', 'ASU120', 'AS80', 'AS120', 'DROP 1KM', 'DROP 2KM', '4KM', '3KM', '2KM']):
        return 280.00
    elif any(k in desc_upper for k in ['ONT', 'ONU', 'ROTEADOR', 'MERCUSYS', 'AX3000', 'AX1500', 'AC1200', 'WIFI 6', 'UNIFI', 'AIR GRID', 'NANOSTATION', 'ROCKET', 'CONVERSOR GIGABIT', 'DCDU', 'MINI RACK']):
        return 125.00
    elif any(k in desc_upper for k in ['CTO', 'CAIXA DE TERMINACAO', 'CAIXA DE EMENDA', 'D.I.O', 'DIO', 'PATCH PANEL', 'SUPORTE BAP', 'BAP 50MM', 'CRUZOETA', 'KIT FERRAMENTA']):
        return 48.00
    elif any(k in desc_upper for k in ['GBIC', 'SFP', 'ALCA PREFORMADA', 'FITA LIBAN', 'FITA DE ACO', 'ISOLADOR', 'CORDOALHA', 'ESTIICADOR', 'DECAPADOR', 'CLEAVER', 'CANETA LASER', 'ATENUADOR']):
        return 28.00
    elif any(k in desc_upper for k in ['CONECTOR', 'ABRACADEIRA', 'PARAFUSO', 'BUCHA', 'PROTETOR', 'ACOPLADOR', 'TUBETE']):
        return 9.50
    return 35.00

def format_tempo_parado(dias):
    if dias is None or dias >= 999:
        return "Sem Giro (> 2 anos / Origem)"
    anos = dias // 365
    meses = (dias % 365) // 30
    if anos > 0:
        if meses > 0:
            return f"{anos} ano{'s' if anos > 1 else ''} e {meses} m{'es' if meses == 1 else 'eses'}"
        return f"{anos} ano{'s' if anos > 1 else ''}"
    elif meses > 0:
        return f"{meses} m{'es' if meses == 1 else 'eses'}"
    else:
        return f"{dias} dias"

def main():
    print("1. Fetching all latest sales from MSSQL S7...")
    s7_conn = pymssql.connect(
        server=os.getenv('DB_S7_HOST'), port=int(os.getenv('DB_S7_PORT', 1433)),
        user=os.getenv('DB_S7_USER'), password=os.getenv('DB_S7_PASSWORD'),
        database=os.getenv('DB_S7_DATABASE'), login_timeout=5, timeout=30
    )
    s7_cur = s7_conn.cursor()

    query = """
        SELECT 
            CODPRODUTO,
            CODEMP,
            MAX(CONVERT(date, DT_PEDIDO, 103)) as DT_ULTIMA_VENDA,
            COUNT(*) as QTD_VENDAS,
            SUM(TRY_CONVERT(numeric(18,2), QTCONVERTIDA)) as VOLUME_VENDIDO
        FROM Relatorios.VW_Logistica_Detalhada
        WHERE OPERACAO = 'SAIDA_BALCAO'
        GROUP BY CODPRODUTO, CODEMP;
    """
    s7_cur.execute(query)
    s7_rows = s7_cur.fetchall()
    print(f"Retrieved {len(s7_rows)} sales records from S7.")
    s7_cur.close()
    s7_conn.close()

    sales_by_filial = {}
    sales_by_network = {}

    for r in s7_rows:
        cod_prod = str(r[0]).strip()
        cod_emp = r[1]
        dt_venda = r[2]
        qtd = r[3]
        vol = float(r[4] or 0)
        
        filial_id = ERP_TO_FILIAL.get(cod_emp)
        if filial_id:
            key = (cod_prod, filial_id)
            if key not in sales_by_filial or dt_venda > sales_by_filial[key]['dt']:
                sales_by_filial[key] = {'dt': dt_venda, 'count': qtd, 'vol': vol}
            else:
                sales_by_filial[key]['count'] += qtd
                sales_by_filial[key]['vol'] += vol

        if cod_prod not in sales_by_network or dt_venda > sales_by_network[cod_prod]['dt']:
            sales_by_network[cod_prod] = {'dt': dt_venda, 'count': qtd}
        else:
            sales_by_network[cod_prod]['count'] += qtd

    # 2. Load audited stock
    print("2. Loading audited physical stock from dashboard_full_data.json...")
    with open('c:/Users/renan.alves/.gemini/Projetos/Bancos/dashboard_full_data.json', 'r', encoding='utf-8') as f:
        full_stock = json.load(f)

    today = date(2026, 9, 28)
    processed_items = []
    resumo_filiais = {}

    for fconfig in full_stock['filiais_config']:
        fid = fconfig['id']
        fnome = fconfig['nome']
        fnome_curto = fconfig['nome_curto']
        flojas = fconfig['lojas']
        fpraca = fconfig['praca']
        
        fdata = full_stock['filiais_data'].get(str(fid), {})
        itens = fdata.get('itens', [])
        
        resumo_filiais[str(fid)] = {
            'nome': fnome,
            'nome_curto': fnome_curto,
            'lojas': flojas,
            'praca': fpraca,
            'total_com_saldo': 0,
            'saldo_total_unidades': 0,
            'valor_imobilizado': 0.0,
            'sem_venda': 0,
            'mais_1ano': 0,
            'semestre': 0,
            'trimestre': 0,
            'mes': 0,
            'recente': 0
        }

        for it in itens:
            cod_sku = str(it['codigo']).strip()
            desc = it.get('produto', '').strip()
            saldo_sn = float(it.get('sn', 0) or 0)
            saldo_wms = float(it.get('wms', 0) or 0)
            
            # Primary reference: SN; fallback to WMS if SN=0
            saldo_fisico = saldo_sn if saldo_sn > 0 else (saldo_wms if saldo_wms > 0 else 0)
            
            # CRITICAL RULE: ONLY PRODUCTS THAT ACTUALLY CONTAIN STOCK IN SYSTEM!
            if saldo_fisico <= 0:
                continue

            resumo_filiais[str(fid)]['total_com_saldo'] += 1
            resumo_filiais[str(fid)]['saldo_total_unidades'] += saldo_fisico

            sale_info = sales_by_filial.get((cod_sku, fid))
            sale_network = sales_by_network.get(cod_sku)

            if sale_info:
                dt_venda = sale_info['dt']
                dias_sem_venda = (today - dt_venda).days
                if dias_sem_venda < 0:
                    dias_sem_venda = 0
                data_venda_str = dt_venda.strftime('%d/%m/%Y')
                data_venda_iso = dt_venda.strftime('%Y-%m-%d')
                status_venda = f"Última venda na filial ({sale_info['count']} pedidos)"
            else:
                dias_sem_venda = 999
                data_venda_str = "Sem Venda na Loja"
                data_venda_iso = "1900-01-01"
                if sale_network:
                    status_venda = f"Sem venda na loja (Última na Rede: {sale_network['dt'].strftime('%d/%m/%Y')})"
                else:
                    status_venda = "Sem Registro de Venda no Sistema"

            valor_unit = estimate_unit_price(desc, cod_sku)
            valor_total = round(saldo_fisico * valor_unit, 2)
            resumo_filiais[str(fid)]['valor_imobilizado'] += valor_total

            if dias_sem_venda >= 999:
                resumo_filiais[str(fid)]['sem_venda'] += 1
            elif dias_sem_venda >= 365:
                resumo_filiais[str(fid)]['mais_1ano'] += 1
            elif dias_sem_venda >= 180:
                resumo_filiais[str(fid)]['semestre'] += 1
            elif dias_sem_venda >= 90:
                resumo_filiais[str(fid)]['trimestre'] += 1
            elif dias_sem_venda >= 30:
                resumo_filiais[str(fid)]['mes'] += 1
            else:
                resumo_filiais[str(fid)]['recente'] += 1

            processed_items.append({
                'c': cod_sku,
                'l': fid,
                'fn': fnome_curto,
                'fl': flojas,
                'd': desc,
                'u': 'UN',
                'sn': saldo_sn,
                'wms': saldo_wms,
                'sf': saldo_fisico,
                'dv': data_venda_str,
                'dvi': data_venda_iso,
                'dias': dias_sem_venda,
                'tp': format_tempo_parado(dias_sem_venda),
                'vu': valor_unit,
                'vt': valor_total,
                'st': status_venda
            })

    processed_items.sort(key=lambda x: (0 if x['dias'] >= 999 else 1, x['dvi'], -x['vt']))

    payload = {
        'data_extracao': today.strftime("%d/%m/%Y"),
        'data_referencia': today.strftime("%Y-%m-%d"),
        'kpis_gerais': {
            'total_skus_com_saldo': len(processed_items),
            'valor_total_imobilizado': round(sum(it['vt'] for it in processed_items), 2),
            'saldo_total_unidades': sum(it['sf'] for it in processed_items),
            'total_sem_venda': sum(1 for it in processed_items if it['dias'] >= 999),
            'total_mais_1ano': sum(1 for it in processed_items if 365 <= it['dias'] < 999),
            'total_semestre': sum(1 for it in processed_items if 180 <= it['dias'] < 365),
            'total_trimestre': sum(1 for it in processed_items if 90 <= it['dias'] < 180),
            'total_mes': sum(1 for it in processed_items if 30 <= it['dias'] < 90),
            'total_recente': sum(1 for it in processed_items if it['dias'] < 30)
        },
        'resumo_por_filial': resumo_filiais,
        'itens': processed_items
    }

    output_file = 'c:/Users/renan.alves/.gemini/Projetos/Bancos/estoque_parado_dataset.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"Successfully generated {output_file} ({len(processed_items)} items)!")

if __name__ == '__main__':
    main()
