import os
import json
import pymysql
import psycopg2
from dotenv import load_dotenv

load_dotenv('c:/Users/renan.alves/.gemini/Projetos/Bancos/.env')

print("Extracting team performance from WMS...")
conn = pymysql.connect(
    host=os.getenv('DB_WMS_HOST'),
    port=int(os.getenv('DB_WMS_PORT', 3306)),
    user=os.getenv('DB_WMS_USER'),
    password=os.getenv('DB_WMS_PASSWORD'),
    database=os.getenv('DB_WMS_DATABASE', 'sistemaestoque'),
    charset='utf8mb4'
)
cur = conn.cursor()

# 1. Ranking de Separacao de Pedidos (vw_separacao_pedidos)
cur.execute("""
    SELECT 
        usuario_separou,
        COUNT(DISTINCT num_pedido) as total_pedidos,
        COUNT(item_id) as total_itens,
        COALESCE(SUM(quantidade_separada), 0) as total_unidades,
        MIN(data_separacao) as primeiro_registro,
        MAX(data_separacao) as ultimo_registro
    FROM vw_separacao_pedidos
    WHERE usuario_separou IS NOT NULL AND usuario_separou != ''
    GROUP BY usuario_separou
    ORDER BY total_pedidos DESC;
""")
ranking_separacao = []
for r in cur.fetchall():
    ranking_separacao.append({
        'usuario': r[0],
        'pedidos': int(r[1]),
        'itens': int(r[2]),
        'unidades': float(r[3]),
        'primeiro': str(r[4]) if r[4] else None,
        'ultimo': str(r[5]) if r[5] else None
    })

# 2. Ranking de Armazenagem / Entrada de Produtos (vw_movimentacoes tipo = 'Entrada')
cur.execute("""
    SELECT 
        usuario_nome,
        usuario_login,
        COUNT(*) as total_movimentacoes,
        COUNT(DISTINCT codigo_produto) as total_skus,
        COALESCE(SUM(quantidade), 0) as total_unidades,
        MIN(data_hora) as primeiro_registro,
        MAX(data_hora) as ultimo_registro
    FROM vw_movimentacoes
    WHERE tipo = 'Entrada' AND usuario_nome IS NOT NULL AND usuario_nome != ''
    GROUP BY usuario_nome, usuario_login
    ORDER BY total_movimentacoes DESC;
""")
ranking_armazenagem = []
for r in cur.fetchall():
    ranking_armazenagem.append({
        'usuario': r[0],
        'login': r[1],
        'movimentacoes': int(r[2]),
        'skus': int(r[3]),
        'unidades': float(r[4]),
        'primeiro': str(r[5]) if r[5] else None,
        'ultimo': str(r[6]) if r[6] else None
    })

# 3. Ranking de Transferencias / Saida (vw_movimentacoes tipo = 'Saída')
cur.execute("""
    SELECT 
        usuario_nome,
        usuario_login,
        COUNT(*) as total_movimentacoes,
        COUNT(DISTINCT codigo_produto) as total_skus,
        COALESCE(SUM(quantidade), 0) as total_unidades,
        MIN(data_hora) as primeiro_registro,
        MAX(data_hora) as ultimo_registro
    FROM vw_movimentacoes
    WHERE tipo = 'Saída' AND usuario_nome IS NOT NULL AND usuario_nome != ''
    GROUP BY usuario_nome, usuario_login
    ORDER BY total_movimentacoes DESC;
""")
ranking_transferencias = []
for r in cur.fetchall():
    ranking_transferencias.append({
        'usuario': r[0],
        'login': r[1],
        'movimentacoes': int(r[2]),
        'skus': int(r[3]),
        'unidades': float(r[4]),
        'primeiro': str(r[5]) if r[5] else None,
        'ultimo': str(r[6]) if r[6] else None
    })

# 4. Recebimento de Mercadorias (vw_recebimento_mercadorias)
cur.execute("""
    SELECT 
        nome_usuario_inicio,
        COUNT(DISTINCT recebimento_id) as total_cargas,
        COUNT(item_id) as total_itens,
        COALESCE(SUM(quantidade_esperada), 0) as total_esperado,
        COALESCE(SUM(quantidade_informada), 0) as total_conferido
    FROM vw_recebimento_mercadorias
    WHERE nome_usuario_inicio IS NOT NULL
    GROUP BY nome_usuario_inicio
    ORDER BY total_cargas DESC;
""")
ranking_recebimento = []
for r in cur.fetchall():
    ranking_recebimento.append({
        'usuario': r[0],
        'cargas': int(r[1]),
        'itens': int(r[2]),
        'esperado': float(r[3]),
        'conferido': float(r[4])
    })

cur.close()
conn.close()

# Also pull romaneios master data for transport
print("Extracting romaneios master data from PostgreSQL...")
pg_conn = psycopg2.connect(
    host=os.getenv('DB_POSTGRES_HOST'),
    port=os.getenv('DB_POSTGRES_PORT', 5432),
    dbname=os.getenv('DB_POSTGRES_DATABASE', 'postgres'),
    user=os.getenv('DB_POSTGRES_USER'),
    password=os.getenv('DB_POSTGRES_PASSWORD')
)
cur = pg_conn.cursor()

cur.execute("""
    SELECT 
        romaneio_id,
        numero_romaneio,
        tipo_direcao,
        status_romaneio,
        filial_origem,
        TO_CHAR(previsao_saida, 'YYYY-MM-DD HH24:MI') as previsao_saida,
        TO_CHAR(data_inicio_viagem, 'YYYY-MM-DD HH24:MI') as data_inicio_viagem,
        motorista_nome,
        veiculo_placa,
        veiculo_modelo,
        total_pedidos_vinculados,
        total_transferencias_vinculadas,
        lista_pedidos_s7,
        lista_tickets_glpi
    FROM powerbi.vw_romaneios_master_completa
    ORDER BY previsao_saida DESC;
""")
romaneios_master = []
for r in cur.fetchall():
    romaneios_master.append({
        'id': r[0],
        'numero': r[1],
        'tipo': r[2],
        'status': r[3],
        'filial': r[4],
        'previsao_saida': r[5],
        'inicio': r[6],
        'motorista': r[7],
        'placa': r[8],
        'modelo': r[9],
        'pedidos': int(r[10] or 0),
        'transferencias': int(r[11] or 0),
        'pedidos_s7': r[12],
        'tickets_glpi': r[13]
    })

# Sample romaneio entregas detalhadas
cur.execute("""
    SELECT 
        romaneio_pedido_id,
        romaneio_id,
        numero_romaneio,
        status_romaneio,
        filial_origem,
        motorista_nome,
        veiculo_placa,
        sequencia_entrega,
        numero_pedido_s7,
        ticket_glpi,
        cliente_nome,
        cliente_cidade,
        transportadora,
        tipo_venda,
        status_entrega_pedido,
        TO_CHAR(data_entrega_conclusao, 'YYYY-MM-DD HH24:MI') as data_entrega,
        recebido_por,
        motivo_ocorrencia,
        observacao_entrega
    FROM powerbi.vw_romaneio_pedidos_detalhada
    ORDER BY romaneio_id DESC, sequencia_entrega ASC;
""")
romaneios_detalhe = []
for r in cur.fetchall():
    romaneios_detalhe.append({
        'id': r[0],
        'romaneio_id': r[1],
        'numero': r[2],
        'status': r[3],
        'filial': r[4],
        'motorista': r[5],
        'placa': r[6],
        'ordem': r[7],
        'pedido_s7': r[8],
        'ticket_glpi': r[9],
        'cliente': r[10],
        'cidade': r[11],
        'transportadora': r[12],
        'tipo_venda': r[13],
        'status_entrega': r[14],
        'data_entrega': r[15],
        'recebido_por': r[16],
        'motivo': r[17],
        'obs': r[18]
    })

cur.close()
pg_conn.close()

team_payload = {
    'separacao': ranking_separacao,
    'armazenagem': ranking_armazenagem,
    'transferencias': ranking_transferencias,
    'recebimento': ranking_recebimento,
    'romaneios_master': romaneios_master,
    'romaneios_detalhe': romaneios_detalhe
}

with open('c:/Users/renan.alves/.gemini/Projetos/Bancos/team_and_transport_data.json', 'w', encoding='utf-8') as f:
    json.dump(team_payload, f, ensure_ascii=False, indent=2)

print(f"Exported team_and_transport_data.json successfully! ({len(ranking_separacao)} separadores, {len(ranking_armazenagem)} armazenadores, {len(ranking_transferencias)} transferencias, {len(romaneios_master)} romaneios master, {len(romaneios_detalhe)} paradas)")
