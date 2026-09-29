"""
Atualizador Oficial de Custos, Aging e Safra de Entrada (SN) de Estoque Parado
GW Wireless - Performance Operacional Logístico
Aplica:
  1. Custos oficiais das planilhas: GW Empresa 01.xls e Fiber Empresa 08.xls para todas as lojas.
  2. Histórico real de vendas (Relatorios.VW_Logistica_Detalhada).
  3. Histórico de movimentações de entrada no ERP S7 (dbo.VW_GW_Movimentacao_Estoque):
     - Data da 1ª entrada registrada no SN
     - Data da última entrada registrada no SN
     - Identificação e cálculo de entradas em 2026 vs entradas até 2025 (ou Legado pré-2025).
Permite desconsiderar tudo o que teve entrada no ano de 2026 e focar no saldo com entrada até 2025.
"""

import os
import json
import shutil
from datetime import datetime, date
import pandas as pd
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

def build_costs_map():
    print("1. Carregando planilhas oficiais de custos S7...")
    df_gw = pd.read_excel('c:/Users/renan.alves/.gemini/Projetos/Bancos/GW Empresa 01.xls')
    df_fiber = pd.read_excel('c:/Users/renan.alves/.gemini/Projetos/Bancos/Fiber Empresa 08.xls')

    costs_map = {}

    # 1. Processar Fiber Empresa 08 primeiro
    for _, row in df_fiber.iterrows():
        sku = str(row['COD_PRODUTO']).strip()
        cm = float(row['CUSTO_MEDIO'] or 0)
        cue = float(row['CUSTO_ULT_ENT'] or 0)
        cman = float(row['CUSTO_MANUAL'] or 0)
        cost = cm if cm > 0 else (cue if cue > 0 else cman)
        un = str(row['UNIDADE'] or 'UN').strip()
        desc = str(row['DESC_PRODUTO'] or '').strip()
        if cost > 0:
            costs_map[sku] = {'cost': round(cost, 4), 'un': un, 'source': 'Fiber Empresa 08', 'desc': desc}

    # 2. Sobrescrever com GW Empresa 01 (Empresa 01 é prioritária)
    for _, row in df_gw.iterrows():
        sku = str(row['COD_PRODUTO']).strip()
        cm = float(row['CUSTO_MEDIO'] or 0)
        cue = float(row['CUSTO_ULT_ENT'] or 0)
        cman = float(row['CUSTO_MANUAL'] or 0)
        cost = cm if cm > 0 else (cue if cue > 0 else cman)
        un = str(row['UNIDADE'] or 'UN').strip()
        desc = str(row['DESC_PRODUTO'] or '').strip()
        if cost > 0:
            costs_map[sku] = {'cost': round(cost, 4), 'un': un, 'source': 'GW Empresa 01', 'desc': desc}

    print(f"Mapa de custos oficiais construído com {len(costs_map)} SKUs únicos.")
    return costs_map

def get_official_cost(sku, desc, costs_map):
    sku_str = str(sku).strip()
    if sku_str in costs_map:
        info = costs_map[sku_str]
        return info['cost'], info['un'], info['source']
    
    # Fallback inteligente baseado em médias de categorias S7 para os 96 SKUs não cadastrados na Matriz/Fiber
    d = (desc or '').upper()
    un = 'UN'
    if '16884' in sku_str:
        cost = 1.25  # Cabo ASU80 fracionado em metros
        un = 'M'
    elif '18451' in sku_str:
        cost = 0.30  # Cabo Drop fracionado em metros
        un = 'M'
    elif 'CABO OPTICO' in d and any(k in d for k in ['ASU', 'AS80', 'AS120', '2KM', '3KM', '4KM']):
        cost = 3500.00
    elif 'DROP' in d and ('1KM' in d or 'COLADO' in d):
        cost = 300.00
    elif any(k in d for k in ['OLT', 'MA5800', 'MA5608T', 'FUSAO', 'OTDR']):
        cost = 1200.00
    elif any(k in d for k in ['ONT', 'ONU', 'ROTEADOR', 'UNIFI', 'AIR FIBER']):
        cost = 165.00
    elif any(k in d for k in ['ALCA', 'LACO', 'ESTICADOR', 'SUPORTE', 'ISOLADOR', 'FRENTE FALSA', 'GABINETE', 'BAP']):
        cost = 3.50
    elif any(k in d for k in ['CONECTOR', 'ABRACADEIRA', 'PIGTAIL', 'CORDAO', 'SPLITTER', 'PROTECAO', 'ACOPLADOR']):
        cost = 6.00
    else:
        cost = 25.00
        
    return cost, un, 'Estimativa Referencial S7'

def main():
    costs_map = build_costs_map()

    print("\n2. Buscando histórico de vendas e entradas no MSSQL S7...")
    s7_conn = pymssql.connect(
        server=os.getenv('DB_S7_HOST'), port=int(os.getenv('DB_S7_PORT', 1433)),
        user=os.getenv('DB_S7_USER'), password=os.getenv('DB_S7_PASSWORD'),
        database=os.getenv('DB_S7_DATABASE'), login_timeout=5, timeout=30
    )
    s7_cur = s7_conn.cursor()

    # VENDAS
    query_vendas = """
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
    s7_cur.execute(query_vendas)
    s7_sales = s7_cur.fetchall()
    print(f"Registros de vendas extraídos do S7: {len(s7_sales)}")

    sales_by_filial = {}
    sales_by_network = {}

    for r in s7_sales:
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

    # ENTRADAS (MOVIMENTAÇÃO DE ESTOQUE)
    print("Extraindo movimentações de entrada (VW_GW_Movimentacao_Estoque)...")
    query_entradas = """
        SELECT 
            COD_PRODUTO, COD_EMPRESA,
            MIN(CONVERT(date, DATA_HORA_MOVIMENTACAO, 103)) as DT_PRI,
            MAX(CONVERT(date, DATA_HORA_MOVIMENTACAO, 103)) as DT_ULT,
            SUM(CASE WHEN YEAR(CONVERT(date, DATA_HORA_MOVIMENTACAO, 103)) <= 2025 THEN QUANTIDADE_MOVIMENTADA ELSE 0 END) as QTD_2025,
            SUM(CASE WHEN YEAR(CONVERT(date, DATA_HORA_MOVIMENTACAO, 103)) = 2026 THEN QUANTIDADE_MOVIMENTADA ELSE 0 END) as QTD_2026,
            COUNT(CASE WHEN YEAR(CONVERT(date, DATA_HORA_MOVIMENTACAO, 103)) = 2026 THEN 1 END) as CNT_2026,
            COUNT(CASE WHEN YEAR(CONVERT(date, DATA_HORA_MOVIMENTACAO, 103)) <= 2025 THEN 1 END) as CNT_2025
        FROM dbo.VW_GW_Movimentacao_Estoque
        WHERE OPERACAO LIKE 'ENTRADA%'
        GROUP BY COD_PRODUTO, COD_EMPRESA;
    """
    s7_cur.execute(query_entradas)
    s7_entries = s7_cur.fetchall()
    print(f"Registros de entrada por filial extraídos: {len(s7_entries)}")
    s7_cur.close()
    s7_conn.close()

    entries_by_sku_filial = {}
    for r in s7_entries:
        sku = str(r[0]).strip()
        emp = r[1]
        fid = ERP_TO_FILIAL.get(emp)
        if not fid:
            continue
        key = (sku, fid)
        if key not in entries_by_sku_filial:
            entries_by_sku_filial[key] = {
                'dt_pri': r[2], 'dt_ult': r[3],
                'q25': r[4] or 0, 'q26': r[5] or 0,
                'c26': r[6] or 0, 'c25': r[7] or 0
            }
        else:
            entries_by_sku_filial[key]['dt_pri'] = min(entries_by_sku_filial[key]['dt_pri'], r[2])
            entries_by_sku_filial[key]['dt_ult'] = max(entries_by_sku_filial[key]['dt_ult'], r[3])
            entries_by_sku_filial[key]['q25'] += (r[4] or 0)
            entries_by_sku_filial[key]['q26'] += (r[5] or 0)
            entries_by_sku_filial[key]['c26'] += (r[6] or 0)
            entries_by_sku_filial[key]['c25'] += (r[7] or 0)

    # 3. Cruzar com inventário auditado das 6 lojas
    print("\n3. Cruzando inventário auditado com custos, vendas e safra de entradas...")
    with open('c:/Users/renan.alves/.gemini/Projetos/Bancos/dashboard_full_data.json', 'r', encoding='utf-8') as f:
        full_stock = json.load(f)

    today = date(2026, 9, 28)
    processed_items = []
    resumo_filiais = {}

    matched_count = 0
    unmatched_count = 0

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
            'recente': 0,
            # Indicadores de Safra (Sem entrada 2026)
            'skus_sem_entrada_2026': 0,
            'unidades_sem_entrada_2026': 0,
            'valor_sem_entrada_2026': 0.0
        }

        for it in itens:
            cod_sku = str(it['codigo']).strip()
            desc = it.get('produto', '').strip()
            saldo_sn = float(it.get('sn', 0) or 0)
            saldo_wms = float(it.get('wms', 0) or 0)
            
            # Referência oficial: Estoque SN; se 0, avalia WMS
            saldo_fisico = saldo_sn if saldo_sn > 0 else (saldo_wms if saldo_wms > 0 else 0)
            
            # REGRA FUNDAMENTAL: Apenas itens com saldo positivo (> 0)
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

            # CUSTO OFICIAL DAS PLANILHAS EXCEL PARA TODAS AS LOJAS
            valor_unit, unidade_prod, fonte_custo = get_official_cost(cod_sku, desc, costs_map)
            valor_total = round(saldo_fisico * valor_unit, 2)
            resumo_filiais[str(fid)]['valor_imobilizado'] += valor_total

            if str(cod_sku) in costs_map:
                matched_count += 1
            else:
                unmatched_count += 1

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

            # SAFRA DE ENTRADAS NO ERP S7
            ent_info = entries_by_sku_filial.get((cod_sku, fid))
            if ent_info:
                dt_pri_ent = ent_info['dt_pri']
                dt_ult_ent = ent_info['dt_ult']
                teve_entrada_2026 = (ent_info['c26'] > 0)
                qtd_entrada_2026 = ent_info['q26']
                qtd_entrada_2025 = ent_info['q25']
                
                pe_str = dt_pri_ent.strftime('%d/%m/%Y')
                pe_iso = dt_pri_ent.strftime('%Y-%m-%d')
                ue_str = dt_ult_ent.strftime('%d/%m/%Y')
                ue_iso = dt_ult_ent.strftime('%Y-%m-%d')
                
                if teve_entrada_2026:
                    safra_status = f"Entrada em 2026 (+{qtd_entrada_2026:,.0f} un)"
                else:
                    safra_status = "Entrada até 2025 (Sem entrada em 2026)"
            else:
                # Saldo físico legado já constava antes de 2025 e não teve novas entradas registradas na filial
                teve_entrada_2026 = False
                qtd_entrada_2026 = 0
                qtd_entrada_2025 = 0
                pe_str = "Legado <= 2024"
                pe_iso = "2024-12-31"
                ue_str = "Legado <= 2024"
                ue_iso = "2024-12-31"
                safra_status = "Legado <= 2024 (Saldo sem entrada 2025/2026)"

            if not teve_entrada_2026:
                resumo_filiais[str(fid)]['skus_sem_entrada_2026'] += 1
                resumo_filiais[str(fid)]['unidades_sem_entrada_2026'] += saldo_fisico
                resumo_filiais[str(fid)]['valor_sem_entrada_2026'] += valor_total

            processed_items.append({
                'c': cod_sku,
                'l': fid,
                'fn': fnome_curto,
                'fl': flojas,
                'd': desc,
                'u': unidade_prod,
                'sn': saldo_sn,
                'wms': saldo_wms,
                'sf': saldo_fisico,
                'dv': data_venda_str,
                'dvi': data_venda_iso,
                'dias': dias_sem_venda,
                'tp': format_tempo_parado(dias_sem_venda),
                'vu': valor_unit,
                'vt': valor_total,
                'st': status_venda,
                'src': fonte_custo,
                # SAFRA DE ENTRADAS NO ERP S7:
                'pe': pe_str,
                'pei': pe_iso,
                'ue': ue_str,
                'uei': ue_iso,
                'e26': teve_entrada_2026,
                'q26': qtd_entrada_2026,
                'q25': qtd_entrada_2025,
                'safra': safra_status
            })

    # Ordenação padrão: data de venda mais antiga no topo (mais crítico primeiro)
    processed_items.sort(key=lambda x: (0 if x['dias'] >= 999 else 1, x['dvi'], -x['vt']))

    # Round dos valores no resumo
    for k in resumo_filiais:
        resumo_filiais[k]['valor_imobilizado'] = round(resumo_filiais[k]['valor_imobilizado'], 2)
        resumo_filiais[k]['valor_sem_entrada_2026'] = round(resumo_filiais[k]['valor_sem_entrada_2026'], 2)

    total_sem_2026 = [it for it in processed_items if not it['e26']]
    total_com_2026 = [it for it in processed_items if it['e26']]

    payload = {
        'data_extracao': today.strftime("%d/%m/%Y"),
        'data_referencia': today.strftime("%Y-%m-%d"),
        'fonte_custos': 'Planilhas Oficiais S7: GW Empresa 01.xls e Fiber Empresa 08.xls (Aplicado a todas as lojas)',
        'cobertura_custos_oficiais': f"{matched_count} de {matched_count + unmatched_count} itens ({matched_count/(matched_count+unmatched_count)*100:.1f}%)",
        'kpis_gerais': {
            # Acervo Completo
            'total_skus_com_saldo': len(processed_items),
            'valor_total_imobilizado': round(sum(it['vt'] for it in processed_items), 2),
            'saldo_total_unidades': sum(it['sf'] for it in processed_items),
            'total_sem_venda': sum(1 for it in processed_items if it['dias'] >= 999),
            'total_mais_1ano': sum(1 for it in processed_items if 365 <= it['dias'] < 999),
            'total_semestre': sum(1 for it in processed_items if 180 <= it['dias'] < 365),
            'total_trimestre': sum(1 for it in processed_items if 90 <= it['dias'] < 180),
            'total_mes': sum(1 for it in processed_items if 30 <= it['dias'] < 90),
            'total_recente': sum(1 for it in processed_items if it['dias'] < 30),
            # Safra: Desconsiderando Entradas em 2026 (Saldo formado até 2025 / Legado)
            'total_sem_entrada_2026': len(total_sem_2026),
            'valor_sem_entrada_2026': round(sum(it['vt'] for it in total_sem_2026), 2),
            'unidades_sem_entrada_2026': sum(it['sf'] for it in total_sem_2026),
            'sem_venda_sem_entrada_2026': sum(1 for it in total_sem_2026 if it['dias'] >= 999),
            'mais_1ano_sem_entrada_2026': sum(1 for it in total_sem_2026 if 365 <= it['dias'] < 999),
            # Safra: Com Entradas em 2026
            'total_com_entrada_2026': len(total_com_2026),
            'valor_com_entrada_2026': round(sum(it['vt'] for it in total_com_2026), 2)
        },
        'resumo_por_filial': resumo_filiais,
        'itens': processed_items
    }

    # Salvar estoque_parado_dataset.json
    output_file = 'c:/Users/renan.alves/.gemini/Projetos/Bancos/estoque_parado_dataset.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"\nSalvo com sucesso {output_file} ({len(processed_items)} registros).")
    print(f"SKUs sem entrada em 2026 (Safra <= 2025): {len(total_sem_2026)} SKUs | R$ {sum(it['vt'] for it in total_sem_2026):,.2f}")

    # Exibir resumo por filial
    print("\n" + "=" * 90)
    print(f"{'Filial':<16} | {'SKUs Total':<10} | {'Sem Entrada 2026':<18} | {'Capital Total':<16} | {'Capital <= 2025':<16}")
    print("-" * 90)
    for fid, res in resumo_filiais.items():
        print(f"{res['nome_curto']:<16} | {res['total_com_saldo']:<10} | {res['skus_sem_entrada_2026']:<18} | R$ {res['valor_imobilizado']:<13,.2f} | R$ {res['valor_sem_entrada_2026']:<13,.2f}")
    print("-" * 90)
    print(f"{'TOTAL REDE':<16} | {payload['kpis_gerais']['total_skus_com_saldo']:<10} | {payload['kpis_gerais']['total_sem_entrada_2026']:<18} | R$ {payload['kpis_gerais']['valor_total_imobilizado']:<13,.2f} | R$ {payload['kpis_gerais']['valor_sem_entrada_2026']:<13,.2f}")
    print("=" * 90)

if __name__ == '__main__':
    main()
