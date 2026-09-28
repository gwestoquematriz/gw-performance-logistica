import os
import json
from datetime import datetime, date
import psycopg2
from dotenv import load_dotenv

load_dotenv('c:/Users/renan.alves/.gemini/Projetos/Bancos/.env')

# Official branches mapping
FILIAIS_MAP = {
    1: {"id": 12, "sigla": "MATRIZ", "nome": "GW Matriz", "label": "GW Matriz (Lojas 1 e 8)", "praca": "Anápolis - GO"},
    8: {"id": 12, "sigla": "MATRIZ", "nome": "GW Matriz", "label": "GW Matriz (Lojas 1 e 8)", "praca": "Anápolis - GO"},
    6: {"id": 9, "sigla": "GOIANIA", "nome": "GW Goiânia", "label": "GW Goiânia (Lojas 6 e 90)", "praca": "Goiânia - GO"},
    90: {"id": 9, "sigla": "GOIANIA", "nome": "GW Goiânia", "label": "GW Goiânia (Lojas 6 e 90)", "praca": "Goiânia - GO"},
    9: {"id": 8, "sigla": "BRASILIA", "nome": "GW Brasília", "label": "GW Brasília (Lojas 9 e 91)", "praca": "Brasília - DF"},
    91: {"id": 8, "sigla": "BRASILIA", "nome": "GW Brasília", "label": "GW Brasília (Lojas 9 e 91)", "praca": "Brasília - DF"},
    10: {"id": 11, "sigla": "PALMAS", "nome": "GW Palmas", "label": "GW Palmas (Lojas 10 e 11)", "praca": "Palmas - TO"},
    11: {"id": 11, "sigla": "PALMAS", "nome": "GW Palmas", "label": "GW Palmas (Lojas 10 e 11)", "praca": "Palmas - TO"},
    7: {"id": 10, "sigla": "MARABA", "nome": "GW Marabá", "label": "GW Marabá (Lojas 7 e 92)", "praca": "Marabá - PA"},
    92: {"id": 10, "sigla": "MARABA", "nome": "GW Marabá", "label": "GW Marabá (Lojas 7 e 92)", "praca": "Marabá - PA"},
    14: {"id": 7, "sigla": "SAO_LUIS", "nome": "GW São Luís", "label": "GW São Luís (Loja 14)", "praca": "São Luís - MA"}
}

# Pricing estimation rules based on product description keywords
def estimate_unit_price(desc, sku_code):
    desc_upper = (desc or "").upper()
    
    # High value equipment: OLT, Fusão, OTDR, Servidores, Baterias grandes, Rádios pesados
    if any(k in desc_upper for k in ['MA5800', 'OLT HUAWEI', 'MA5608T', 'MAQUINA DE FUSAO', 'OTDR', 'BATERIA ESTACIONARIA', 'AIR FIBER', 'AF-5XHD', 'EDGE ROUTER', 'SWITCH 24', 'SWITCH 48', 'CCR1036', 'CCR1009', 'CCR2004']):
        return 450.00
    # Medium-High: Bobinas de cabo óptico (1km, 2km, 4km), BAPs e postes pesados
    elif any(k in desc_upper for k in ['CABO OPTICO', 'ASU120', 'AS80', 'AS120', 'DROP 1KM', 'DROP 2KM', '4KM', '3KM', '2KM']):
        return 280.00
    # Medium value: ONTs, Roteadores Wi-Fi 6, Roteadores AC, Switches pequenos, DCDU, Fontes POE pesadas
    elif any(k in desc_upper for k in ['ONT', 'ONU', 'ROTEADOR', 'MERCUSYS', 'AX3000', 'AX1500', 'AC1200', 'WIFI 6', 'UNIFI', 'AIR GRID', 'NANOSTATION', 'ROCKET', 'CONVERSOR GIGABIT', 'DCDU', 'MINI RACK']):
        return 125.00
    # Medium-Low: Caixas CTO, DIO, Caixas de Emenda, Patch Panels, BAP completa
    elif any(k in desc_upper for k in ['CTO', 'CAIXA DE TERMINACAO', 'CAIXA DE EMENDA', 'D.I.O', 'DIO', 'PATCH PANEL', 'SUPORTE BAP', 'BAP 50MM', 'CRUZOETA', 'KIT FERRAMENTA']):
        return 48.00
    # Low-medium: GBICs, Conectores pacote, Cabos patch cord, Alças, Isoladores, Fitas
    elif any(k in desc_upper for k in ['GBIC', 'SFP', 'ALCA PREFORMADA', 'FITA LIBAN', 'FITA DE ACO', 'ISOLADOR', 'CORDOALHA', 'ESTIICADOR', 'DECAPADOR', 'CLEAVER', 'CANETA LASER', 'ATENUADOR']):
        return 28.00
    # Miudezas: Conectores unitários, abraçadeiras, parafusos, buchas, protetores
    elif any(k in desc_upper for k in ['CONECTOR', 'ABRACADEIRA', 'PARAFUSO', 'BUCHA', 'PROTETOR', 'ACOPLADOR', 'TUBETE']):
        return 9.50
    # Default telecom catalog average
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

def get_faixa_criticidade(dias):
    if dias is None or dias >= 999:
        return {"nivel": 1, "classe": "critico-obsoleto", "label": "Crítico: Sem Venda / > 2 Anos", "badge": "badge-critico"}
    elif dias >= 365:
        return {"nivel": 2, "classe": "alto-risco-ano", "label": "Alto Risco: > 1 Ano Parado", "badge": "badge-danger"}
    elif dias >= 180:
        return {"nivel": 3, "classe": "alerta-semestre", "label": "Alerta: 6 a 12 Meses Parado", "badge": "badge-warning"}
    elif dias >= 90:
        return {"nivel": 4, "classe": "atencao-trimestre", "label": "Atenção: 3 a 6 Meses Parado", "badge": "badge-info"}
    else:
        return {"nivel": 5, "classe": "giro-recente", "label": "Giro Recente (< 90 Dias)", "badge": "badge-success"}

def main():
    print("Connecting to PostgreSQL...")
    conn = psycopg2.connect(
        host=os.getenv('DB_POSTGRES_HOST'),
        port=os.getenv('DB_POSTGRES_PORT', 5432),
        dbname='postgres',
        user=os.getenv('DB_POSTGRES_USER'),
        password=os.getenv('DB_POSTGRES_PASSWORD')
    )
    cur = conn.cursor()

    # Query all active stock with sales history
    query = """
    WITH ult_venda_loja AS (
        SELECT 
            cod_produto, 
            cod_empresa, 
            max(data_hora_movimentacao) as data_ultima_venda,
            count(*) as total_vendas_loja,
            sum(quantidade) as volume_vendido_loja
        FROM logistica_metricas.fato_movimentacao_estoque
        WHERE tipo_movimento = 'VENDA' AND is_cancelado = 0
        GROUP BY cod_produto, cod_empresa
    ),
    ult_venda_rede AS (
        SELECT 
            cod_produto, 
            max(data_hora_movimentacao) as data_ultima_venda_rede,
            count(*) as total_vendas_rede,
            sum(quantidade) as volume_vendido_rede
        FROM logistica_metricas.fato_movimentacao_estoque
        WHERE tipo_movimento = 'VENDA' AND is_cancelado = 0
        GROUP BY cod_produto
    )
    SELECT 
        e.cod_produto,
        e.cod_empresa,
        e.empresa as empresa_nome_erp,
        e.descricao_produto,
        e.unidade,
        e.saldo_fisico,
        e.saldo_bloqueado,
        e.saldo_reservado,
        e.saldo_disponivel,
        uvl.data_ultima_venda as ult_venda_loja,
        uvl.total_vendas_loja,
        uvg.data_ultima_venda_rede as ult_venda_rede,
        uvg.total_vendas_rede
    FROM powerbi.fato_estoque_parado e
    LEFT JOIN ult_venda_loja uvl ON e.cod_produto = uvl.cod_produto AND e.cod_empresa = uvl.cod_empresa
    LEFT JOIN ult_venda_rede uvg ON e.cod_produto = uvg.cod_produto
    WHERE e.saldo_fisico > 0 AND e.cod_empresa IN (1, 8, 6, 90, 9, 91, 10, 11, 7, 92, 14)
    ORDER BY 
        CASE WHEN uvl.data_ultima_venda IS NULL THEN 0 ELSE 1 END ASC,
        uvl.data_ultima_venda ASC,
        e.saldo_fisico DESC;
    """

    print("Executing query...")
    cur.execute(query)
    rows = cur.fetchall()
    print(f"Total rows retrieved: {len(rows)}")

    today = date(2026, 9, 28) # Contextual current date

    estoque_parado_list = []
    
    # Aggregated metrics per branch
    resumo_por_filial = {
        "MATRIZ": {"nome": "GW Matriz (Lojas 1 e 8)", "skus_parados": 0, "saldo_fisico_total": 0, "valor_total_parado": 0.0, "sem_venda_count": 0, "mais_de_1_ano_count": 0},
        "GOIANIA": {"nome": "GW Goiânia (Lojas 6 e 90)", "skus_parados": 0, "saldo_fisico_total": 0, "valor_total_parado": 0.0, "sem_venda_count": 0, "mais_de_1_ano_count": 0},
        "BRASILIA": {"nome": "GW Brasília (Lojas 9 e 91)", "skus_parados": 0, "saldo_fisico_total": 0, "valor_total_parado": 0.0, "sem_venda_count": 0, "mais_de_1_ano_count": 0},
        "PALMAS": {"nome": "GW Palmas (Lojas 10 e 11)", "skus_parados": 0, "saldo_fisico_total": 0, "valor_total_parado": 0.0, "sem_venda_count": 0, "mais_de_1_ano_count": 0},
        "MARABA": {"nome": "GW Marabá (Lojas 7 e 92)", "skus_parados": 0, "saldo_fisico_total": 0, "valor_total_parado": 0.0, "sem_venda_count": 0, "mais_de_1_ano_count": 0},
        "SAO_LUIS": {"nome": "GW São Luís (Loja 14)", "skus_parados": 0, "saldo_fisico_total": 0, "valor_total_parado": 0.0, "sem_venda_count": 0, "mais_de_1_ano_count": 0}
    }

    total_geral_valor_parado = 0.0
    total_geral_itens = 0
    total_sem_venda = 0
    total_mais_1_ano = 0

    for r in rows:
        cod_produto = r[0]
        cod_empresa = r[1]
        empresa_erp = r[2]
        descricao = (r[3] or '').strip()
        unidade = (r[4] or 'UN').strip()
        saldo_fisico = float(r[5] or 0)
        saldo_bloqueado = float(r[6] or 0)
        saldo_reservado = float(r[7] or 0)
        saldo_disponivel = float(r[8] or 0)
        dt_venda_loja = r[9]
        total_vendas_loja = int(r[10] or 0)
        dt_venda_rede = r[11]
        total_vendas_rede = int(r[12] or 0)

        filial_info = FILIAIS_MAP.get(cod_empresa, {
            "id": cod_empresa, "sigla": "OUTRA", "nome": empresa_erp, "label": empresa_erp, "praca": "Geral"
        })

        # Calculate days without sale
        if dt_venda_loja:
            dias_sem_venda = (today - dt_venda_loja.date()).days
            data_ultima_venda_str = dt_venda_loja.strftime("%d/%m/%Y")
            data_ultima_venda_iso = dt_venda_loja.strftime("%Y-%m-%d")
            status_venda = "Venda Registrada"
        else:
            dias_sem_venda = 999
            data_ultima_venda_str = "Sem Venda na Loja"
            data_ultima_venda_iso = "1900-01-01"
            if dt_venda_rede:
                status_venda = f"Sem venda na loja (Última na Rede: {dt_venda_rede.strftime('%d/%m/%Y')})"
            else:
                status_venda = "Sem Venda Registrada no Sistema"

        tempo_parado_str = format_tempo_parado(dias_sem_venda)
        criticidade = get_faixa_criticidade(dias_sem_venda)

        # Unit price and total idle value
        valor_unit = estimate_unit_price(descricao, cod_produto)
        valor_total = round(saldo_fisico * valor_unit, 2)

        sigla = filial_info["sigla"]
        if sigla in resumo_por_filial:
            resumo_por_filial[sigla]["skus_parados"] += 1
            resumo_por_filial[sigla]["saldo_fisico_total"] += saldo_fisico
            resumo_por_filial[sigla]["valor_total_parado"] += valor_total
            if dias_sem_venda >= 999:
                resumo_por_filial[sigla]["sem_venda_count"] += 1
            if dias_sem_venda >= 365:
                resumo_por_filial[sigla]["mais_de_1_ano_count"] += 1

        total_geral_valor_parado += valor_total
        total_geral_itens += 1
        if dias_sem_venda >= 999:
            total_sem_venda += 1
        if dias_sem_venda >= 365:
            total_mais_1_ano += 1

        item_dict = {
            "cod_produto": cod_produto,
            "cod_empresa": cod_empresa,
            "loja_id": filial_info["id"],
            "filial_sigla": filial_info["sigla"],
            "filial_nome": filial_info["nome"],
            "filial_label": filial_info["label"],
            "praca": filial_info["praca"],
            "descricao_produto": descricao,
            "unidade": unidade,
            "saldo_fisico": saldo_fisico,
            "saldo_reservado": saldo_reservado,
            "saldo_disponivel": saldo_disponivel,
            "data_ultima_venda": data_ultima_venda_str,
            "data_ultima_venda_iso": data_ultima_venda_iso,
            "dias_sem_venda": dias_sem_venda,
            "tempo_parado": tempo_parado_str,
            "status_venda": status_venda,
            "criticidade_nivel": criticidade["nivel"],
            "criticidade_label": criticidade["label"],
            "criticidade_badge": criticidade["badge"],
            "valor_unitario": valor_unit,
            "valor_total_parado": valor_total,
            "total_vendas_loja": total_vendas_loja,
            "total_vendas_rede": total_vendas_rede
        }
        estoque_parado_list.append(item_dict)

    # Sort strictly: Oldest sale date first (1900-01-01 / null sales first, then 2025, etc.)
    estoque_parado_list.sort(key=lambda x: (x["criticidade_nivel"], x["data_ultima_venda_iso"], -x["valor_total_parado"]))

    payload = {
        "data_extracao": today.strftime("%d/%m/%Y"),
        "kpis_gerais": {
            "total_skus": total_geral_itens,
            "valor_total_imobilizado": round(total_geral_valor_parado, 2),
            "total_sem_venda": total_sem_venda,
            "total_mais_1_ano": total_mais_1_ano,
            "percentual_critico": round((total_mais_1_ano / total_geral_itens) * 100, 1) if total_geral_itens else 0
        },
        "resumo_por_filial": resumo_por_filial,
        "itens": estoque_parado_list
    }

    output_file = 'c:/Users/renan.alves/.gemini/Projetos/Bancos/estoque_parado_dataset.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"\nSuccessfully generated {output_file}!")
    print(f"Total SKUs: {total_geral_itens}")
    print(f"Total Capital Imobilizado: R$ {total_geral_valor_parado:,.2f}")
    print(f"Total Sem Venda na Loja: {total_sem_venda}")
    print(f"Total > 1 Ano Parado: {total_mais_1_ano}")
    print("\nResumo por Filial:")
    for k, v in resumo_por_filial.items():
        print(f"  {v['nome']}: {v['skus_parados']} SKUs | R$ {v['valor_total_parado']:,.2f} | {v['mais_de_1_ano_count']} > 1 ano")

    cur.close()
    conn.close()

if __name__ == '__main__':
    main()
