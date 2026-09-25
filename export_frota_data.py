import os
import json
import psycopg2
import pymysql
from dotenv import load_dotenv

load_dotenv('c:/Users/renan.alves/.gemini/Projetos/Bancos/.env')

pg_conn = psycopg2.connect(
    host=os.getenv('DB_POSTGRES_HOST'),
    port=os.getenv('DB_POSTGRES_PORT', 5432),
    dbname=os.getenv('DB_POSTGRES_DATABASE', 'gwlogistica'),
    user=os.getenv('DB_POSTGRES_USER'),
    password=os.getenv('DB_POSTGRES_PASSWORD')
)
cur = pg_conn.cursor()

# 1. Total overview by vehicle
cur.execute("""
    SELECT 
        v.placa, v.modelo, v.apelido, v.status, v.ano_modelo,
        v.filial_atual, v.motorista_atual,
        COALESCE(v.total_gasto_combustivel, 0) as gasto_combustivel,
        COALESCE(v.total_litros_consumidos, 0) as litros,
        COALESCE(v.km_total_rodado, 0) as km_rodado,
        COALESCE(v.media_km_litro_geral, 0) as media_kml,
        COALESCE(v.total_gasto_pedagio, 0) as gasto_pedagio,
        COALESCE(v.qtd_passagens_pedagio, 0) as qtd_pedagio,
        COALESCE(v.total_gasto_manutencao, 0) as gasto_manutencao,
        COALESCE(v.custo_total_veiculo, 0) as custo_total
    FROM powerbi.vw_frota_visao_geral v
    ORDER BY v.custo_total_veiculo DESC;
""")
veiculos = []
for r in cur.fetchall():
    veiculos.append({
        'placa': r[0], 'modelo': r[1], 'apelido': r[2], 'status': r[3],
        'ano_modelo': r[4], 'filial': r[5] or 'MATRIZ', 'motorista': r[6] or 'N/D',
        'gasto_combustivel': float(r[7]), 'litros': float(r[8]), 'km_rodado': float(r[9]),
        'media_kml': float(r[10]), 'gasto_pedagio': float(r[11]), 'qtd_pedagio': int(r[12]),
        'gasto_manutencao': float(r[13]), 'custo_total': float(r[14])
    })
print(f"Total veiculos: {len(veiculos)}")

# 2. Monthly costs evolution
cur.execute("""
    SELECT ano_mes, filial, placa, apelido, categoria_custo, SUM(valor_total) as valor
    FROM powerbi.vw_frota_custos_consolidados
    GROUP BY ano_mes, filial, placa, apelido, categoria_custo
    ORDER BY ano_mes, filial, placa;
""")
custos_mensais = []
for r in cur.fetchall():
    cat = r[4].upper().strip()
    if 'ABASTEC' in cat:
        cat_padrao = 'COMBUSTÍVEL'
    elif 'PEDAG' in cat:
        cat_padrao = 'PEDÁGIO'
    elif 'PEÇ' in cat or 'PEC' in cat:
        cat_padrao = 'PEÇAS'
    elif 'MANUTEN' in cat:
        cat_padrao = 'MANUTENÇÃO'
    elif 'SERVI' in cat:
        cat_padrao = 'SERVIÇOS'
    else:
        cat_padrao = 'OUTROS'
        
    custos_mensais.append({
        'ano_mes': r[0],
        'filial': r[1] or 'MATRIZ',
        'placa': r[2],
        'apelido': r[3],
        'categoria': cat_padrao,
        'valor': float(r[5])
    })
print(f"Total registros custos mensais: {len(custos_mensais)}")

# 3. Monthly fuel details (litros, km, kml, custo)
cur.execute("""
    SELECT 
        TO_CHAR(data_abastecimento, 'YYYY-MM') as ano_mes,
        placa,
        COUNT(*) as qtd_abastecimentos,
        SUM(valor_pago) as valor_total,
        SUM(litros) as litros_total,
        SUM(km_rodado) as km_total,
        AVG(preco_bomba) as preco_medio_litro,
        CASE WHEN SUM(litros) > 0 THEN SUM(km_rodado) / SUM(litros) ELSE 0 END as kml_medio
    FROM powerbi.fato_abastecimentos
    WHERE data_abastecimento IS NOT NULL
    GROUP BY TO_CHAR(data_abastecimento, 'YYYY-MM'), placa
    ORDER BY ano_mes, placa;
""")
combustivel_mensal = []
for r in cur.fetchall():
    combustivel_mensal.append({
        'ano_mes': r[0],
        'placa': r[1],
        'qtd': int(r[2]),
        'valor': float(r[3] or 0),
        'litros': float(r[4] or 0),
        'km': float(r[5] or 0),
        'preco_medio': round(float(r[6] or 0), 3),
        'kml': round(float(r[7] or 0), 2)
    })
print(f"Total registros combustivel mensal: {len(combustivel_mensal)}")

# 4. Maintenance breakdown
cur.execute("""
    SELECT 
        id_despesa,
        TO_CHAR(data_despesa, 'YYYY-MM-DD') as data_despesa,
        TO_CHAR(data_despesa, 'YYYY-MM') as ano_mes,
        placa,
        veiculo_descricao,
        grupo,
        descricao,
        filial_efetiva,
        cidade,
        valor
    FROM powerbi.fato_manutencoes_despesas
    ORDER BY data_despesa DESC;
""")
manutencoes = []
for r in cur.fetchall():
    grp = (r[5] or '').upper().strip()
    if 'PEÇ' in grp or 'PEC' in grp:
        tipo = 'PEÇAS'
    elif 'SERV' in grp:
        tipo = 'SERVIÇOS'
    elif 'MANUT' in grp:
        tipo = 'MANUTENÇÃO'
    else:
        tipo = 'OUTROS'

    manutencoes.append({
        'id': r[0],
        'data': r[1],
        'ano_mes': r[2],
        'placa': r[3],
        'veiculo': r[4],
        'grupo': tipo,
        'descricao': r[6] or '',
        'filial': r[7] or 'MATRIZ',
        'cidade': r[8] or '',
        'valor': float(r[9] or 0)
    })
print(f"Total manutencoes detalhadas: {len(manutencoes)}")

# 5. Pedagios breakdown
cur.execute("""
    SELECT 
        TO_CHAR(data_passagem, 'YYYY-MM') as ano_mes,
        placa,
        filial_efetiva,
        COUNT(*) as passagens,
        SUM(valor_cobrado) as valor_total,
        estabelecimento
    FROM powerbi.fato_pedagios
    WHERE data_passagem IS NOT NULL
    GROUP BY TO_CHAR(data_passagem, 'YYYY-MM'), placa, filial_efetiva, estabelecimento
    ORDER BY ano_mes DESC;
""")
pedagios_agrupados = []
for r in cur.fetchall():
    pedagios_agrupados.append({
        'ano_mes': r[0],
        'placa': r[1],
        'filial': r[2] or 'MATRIZ',
        'passagens': int(r[3]),
        'valor': float(r[4] or 0),
        'estabelecimento': r[5] or 'N/D'
    })
print(f"Total registros agrupados pedagios: {len(pedagios_agrupados)}")

# 6. GLPI Abastecimento Transfers
cur.execute("""
    SELECT 
        id_chamado, titulo_chamado, status_chamado, 
        TO_CHAR(data_abertura, 'YYYY-MM-DD HH24:MI') as data_abertura,
        solicitante_nome, empresa_origem, empresa_destino, motivo
    FROM powerbi.glpi_transferencia_abastecimento
    ORDER BY id_chamado DESC;
""")
glpi_transfers = []
for r in cur.fetchall():
    glpi_transfers.append({
        'id': r[0],
        'titulo': r[1],
        'status': r[2],
        'data': r[3],
        'solicitante': r[4],
        'origem': r[5],
        'destino': r[6],
        'motivo': r[7]
    })
print(f"Total glpi transfers: {len(glpi_transfers)}")

cur.close()
pg_conn.close()

# Save complete JSON
dataset = {
    'veiculos': veiculos,
    'custos_mensais': custos_mensais,
    'combustivel_mensal': combustivel_mensal,
    'manutencoes': manutencoes,
    'pedagios_agrupados': pedagios_agrupados,
    'glpi_transfers': glpi_transfers
}

with open('c:/Users/renan.alves/.gemini/Projetos/Bancos/frota_dashboard_data.json', 'w', encoding='utf-8') as f:
    json.dump(dataset, f, ensure_ascii=False, indent=2)

print("frota_dashboard_data.json exported successfully!")
