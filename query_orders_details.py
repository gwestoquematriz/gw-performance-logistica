import os
import pymssql
import pymysql
from dotenv import load_dotenv

load_dotenv('c:/Users/renan.alves/.gemini/Projetos/Bancos/.env')

pedidos = [637210, 624850, 619871, 615696, 633388, 626019, 629207, 641704, 615313, 642089, 631048]

s7_conn = pymssql.connect(
    server=os.getenv('DB_S7_HOST'), port=int(os.getenv('DB_S7_PORT', 1433)),
    user=os.getenv('DB_S7_USER'), password=os.getenv('DB_S7_PASSWORD'),
    database=os.getenv('DB_S7_DATABASE'), login_timeout=5, timeout=30
)
s7_cur = s7_conn.cursor()

wms_conn = pymysql.connect(
    host=os.getenv('DB_WMS_HOST'), port=int(os.getenv('DB_WMS_PORT', 3306)),
    user=os.getenv('DB_WMS_USER'), password=os.getenv('DB_WMS_PASSWORD'),
    database=os.getenv('DB_WMS_DATABASE', 'sistemaestoque'), charset='utf8mb4'
)
wms_cur = wms_conn.cursor()

for ped in pedidos:
    print(f"\n==================== PEDIDO {ped} ====================")
    # 1. S7 VW_Logistica_Detalhada
    s7_cur.execute(f"""
        SELECT CODEMP, EMPRESA, DT_PEDIDO, CLIENTE, VENDEDOR, CODPRODUTO, PRODUTO, QTCONVERTIDA, UNIDADE, OPERACAO
        FROM Relatorios.VW_Logistica_Detalhada
        WHERE NUMPEDIDOVENDA = {ped}
        ORDER BY CODPRODUTO;
    """)
    rows_s7 = s7_cur.fetchall()
    print(f"  [S7 VW_Logistica_Detalhada] {len(rows_s7)} itens encontrados:")
    for r in rows_s7:
        print(f"    Emp {r[0]} ({r[1]}) | Data: {r[2]} | Cliente: {r[3]} | Vend: {r[4]} | SKU: {r[5]} | Qtd: {r[7]} {r[8]} | {r[6]}")

    # If not in Detalhada, check Logistica_Pedidos
    if not rows_s7:
        s7_cur.execute(f"""
            SELECT CODEMP, EMPRESA, DT_PEDIDO, CLIENTE, OPERACAO
            FROM Relatorios.Logistica_Pedidos
            WHERE NUM_PEDVENDA = {ped}
        """)
        rows_lp = s7_cur.fetchall()
        print(f"  [S7 Logistica_Pedidos] {rows_lp}")

    # Check VW_GW_Movimentacao_Estoque
    s7_cur.execute(f"""
        SELECT COD_EMPRESA, EMPRESA, DATA_HORA_MOVIMENTACAO, COD_PRODUTO, PRODUTO, QUANTIDADE_MOVIMENTADA, OPERACAO, NUM_NOTA
        FROM dbo.VW_GW_Movimentacao_Estoque
        WHERE NUM_PEDIDO = {ped}
    """)
    rows_mov = s7_cur.fetchall()
    print(f"  [S7 Movimentacoes] {len(rows_mov)} registros:")
    for r in rows_mov:
        print(f"    Emp {r[0]} ({r[1]}) | Data: {r[2]} | NF: {r[7]} | SKU: {r[3]} | Qtd: {r[5]} | {r[4]}")

    # 2. WMS
    wms_cur.execute(f"""
        SELECT cliente, vendedor, data_separacao, cod_produto, nome_produto, quantidade_pedido, quantidade_separada, quantidade_pendente, status_geral
        FROM vw_separacao_pedidos
        WHERE num_pedido = '{ped}'
        ORDER BY cod_produto;
    """)
    rows_wms = wms_cur.fetchall()
    print(f"  [WMS vw_separacao_pedidos] {len(rows_wms)} itens encontrados:")
    for r in rows_wms:
        print(f"    Cliente: {r[0]} | Vend: {r[1]} | Data: {r[2]} | SKU: {r[3]} | Pedido: {r[5]} | Entregue/Sep: {r[6]} | Pendente: {r[7]} | {r[4]}")

s7_conn.close()
wms_conn.close()
