import os
import pymssql
from dotenv import load_dotenv
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, Protection
from openpyxl.utils import get_column_letter

load_dotenv('c:/Users/renan.alves/.gemini/Projetos/Bancos/.env')

excel_path = 'c:/Users/renan.alves/.gemini/Projetos/Bancos/Gestao_Ocorrencias_Pedidos_GW_Fiber.xlsx'

print("1. Conectando ao SQL Server S7...")
s7_conn = pymssql.connect(
    server=os.getenv('DB_S7_HOST'),
    port=int(os.getenv('DB_S7_PORT', 1433)),
    user=os.getenv('DB_S7_USER'),
    password=os.getenv('DB_S7_PASSWORD'),
    database=os.getenv('DB_S7_DATABASE'),
    login_timeout=10,
    timeout=60
)
s7_cur = s7_conn.cursor()

print("2. Extraindo pedidos de 2026 de Relatorios.VW_Logistica_Detalhada...")
query_s7 = """
    SELECT 
        NUMPEDIDOVENDA,
        CODEMP,
        EMPRESA,
        CONVERT(varchar, TRY_CONVERT(date, DT_PEDIDO, 103), 103) as DT_FATURAMENTO,
        CLIENTE,
        VENDEDOR,
        CODPRODUTO,
        PRODUTO,
        TRY_CONVERT(numeric(18,2), QTCONVERTIDA) as QTD_PEDIDO,
        UNIDADE,
        OPERACAO
    FROM Relatorios.VW_Logistica_Detalhada
    WHERE TRY_CONVERT(date, DT_PEDIDO, 103) >= '2026-01-01'
    ORDER BY NUMPEDIDOVENDA DESC, CODPRODUTO ASC;
"""
s7_cur.execute(query_s7)
rows_db = s7_cur.fetchall()
print(f"   -> {len(rows_db)} itens de pedidos carregados do S7 para a Base de Dados.")
s7_conn.close()

# Iniciar Workbook
wb = openpyxl.Workbook()

# Sheet 1: Gestão de Ocorrências
ws_oc = wb.active
ws_oc.title = "Gestão de Ocorrências"
ws_oc.views.sheetView[0].showGridLines = True

# Sheet 2: Base de Dados
ws_db = wb.create_sheet(title="Base de Dados")
ws_db.views.sheetView[0].showGridLines = True

# Paleta Visual Corporativa GW & Fiber
DARK_NAVY = "1B365D"
TITLE_NAVY = "0F2537"
HEADER_FILL = PatternFill(start_color=DARK_NAVY, end_color=DARK_NAVY, fill_type="solid")
TITLE_FILL = PatternFill(start_color=TITLE_NAVY, end_color=TITLE_NAVY, fill_type="solid")
SUBTITLE_FILL = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
ZEBRA_FILL = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
WHITE_FILL = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
INPUT_FILL = PatternFill(start_color="FFFBEB", end_color="FFFBEB", fill_type="solid") # Amarelo/âmbar suave para campos editáveis
AUTO_FILL = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")  # Cinza suave para campos bloqueados

# Cores de Status
STATUS_COLORS = {
    "Furo de Estoque": {"fill": "FCE8E6", "font": "C5221F"},
    "Mercadoria Encontrada": {"fill": "E6F4EA", "font": "137333"},
    "Aguardando Vendedor": {"fill": "FEF7E0", "font": "B06000"},
    "Item Personalizado": {"fill": "F3E8FD", "font": "7627BB"},
    "Projeto em Aprovação": {"fill": "E8F0FE", "font": "1A73E8"}
}

thin_border_side = Side(style='thin', color='E2E8F0')
THIN_BORDER = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)
HEADER_BORDER = Border(
    left=Side(style='thin', color='CBD5E1'),
    right=Side(style='thin', color='CBD5E1'),
    top=Side(style='medium', color='0F2537'),
    bottom=Side(style='medium', color='0F2537')
)

# ----------------------------------------------------
# 3. Preencher Aba "Base de Dados"
# ----------------------------------------------------
print("3. Preenchendo a aba 'Base de Dados'...")
db_headers = [
    "CHAVE_BUSCA", "NUM_PEDIDO", "COD_EMPRESA", "EMPRESA_NOME", 
    "REFERENCIA_EMPRESA", "CLIENTE", "VENDEDOR", "DATA_FATURAMENTO", 
    "COD_MATERIAL", "DESCRICAO", "TOTAL_PEDIDO", "UNIDADE", "OPERACAO"
]
ws_db.append(db_headers)

header_font = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
for col_idx in range(1, len(db_headers) + 1):
    cell = ws_db.cell(row=1, column=col_idx)
    cell.fill = HEADER_FILL
    cell.font = header_font
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cell.border = HEADER_BORDER
    cell.protection = Protection(locked=True)
ws_db.row_dimensions[1].height = 28

for r_idx, r in enumerate(rows_db, start=2):
    numped = int(r[0]) if r[0] is not None else 0
    codemp = int(r[1]) if r[1] is not None else 0
    emp_nome = str(r[2]).strip() if r[2] else ""
    dt_fat = str(r[3]).strip() if r[3] else ""
    cliente = str(r[4]).strip() if r[4] else ""
    vendedor = str(r[5]).strip() if r[5] else ""
    codmat = int(r[6]) if (r[6] is not None and str(r[6]).isdigit()) else str(r[6] or "")
    descricao = str(r[7]).strip() if r[7] else ""
    total = float(r[8]) if r[8] is not None else 0.0
    unidade = str(r[9]).strip() if r[9] else "UN"
    operacao = str(r[10]).strip() if r[10] else ""
    
    # Determinar Referência GW vs Fiber
    emp_brand = "Fiber" if "FIBER" in emp_nome.upper() else "GW"
    ref_empresa = f"{emp_brand} (Empresa {codemp:02d})"
    chave_busca = f"{numped}_{codmat}"

    ws_db.append([
        chave_busca,
        numped,
        codemp,
        emp_nome,
        ref_empresa,
        cliente,
        vendedor,
        dt_fat,
        codmat,
        descricao,
        total,
        unidade,
        operacao
    ])

# Ajustar colunas da Base de Dados
for col in ws_db.columns:
    max_len = max(len(str(cell.value or '')) for cell in col[:100])
    col_letter = get_column_letter(col[0].column)
    ws_db.column_dimensions[col_letter].width = max(max_len + 3, 12)

ws_db.column_dimensions['A'].width = 16
ws_db.column_dimensions['D'].width = 24
ws_db.column_dimensions['E'].width = 20
ws_db.column_dimensions['F'].width = 38
ws_db.column_dimensions['G'].width = 22
ws_db.column_dimensions['J'].width = 42

# Bloquear e proteger a aba Base de Dados contra qualquer alteração acidental
ws_db.protection.sheet = True
ws_db.protection.enable()

# ----------------------------------------------------
# 4. Preencher Aba "Gestão de Ocorrências"
# ----------------------------------------------------
print("4. Montando a aba 'Gestão de Ocorrências'...")

# Banner do Título
ws_oc.merge_cells('A1:L1')
title_cell = ws_oc['A1']
title_cell.value = "GW WIRELLES & FIBER TELECOM — PAINEL DE GESTÃO DE OCORRÊNCIAS DE PEDIDOS"
title_cell.font = Font(name="Segoe UI", size=13, bold=True, color="FFFFFF")
title_cell.fill = TITLE_FILL
title_cell.alignment = Alignment(horizontal="center", vertical="center")
title_cell.protection = Protection(locked=True)
ws_oc.row_dimensions[1].height = 36

# Banner de Instruções com destaque para proteção de células
ws_oc.merge_cells('A2:L2')
sub_cell = ws_oc['A2']
sub_cell.value = "🔒 PROTEÇÃO ATIVA: Digitação permitida APENAS nos campos editáveis (Nº Pedido, Cód. Material, Qtd Entregue e Observação). As demais colunas são preenchidas automaticamente pela Base de Dados e estão bloqueadas para evitar erros de fórmulas."
sub_cell.font = Font(name="Segoe UI", size=9, bold=True, color="1E293B")
sub_cell.fill = SUBTITLE_FILL
sub_cell.alignment = Alignment(horizontal="left", vertical="center", indent=1)
sub_cell.protection = Protection(locked=True)
ws_oc.row_dimensions[2].height = 26

ws_oc.row_dimensions[3].height = 10 # Espaçador
for c in range(1, 13):
    ws_oc.cell(row=3, column=c).protection = Protection(locked=True)

# Cabeçalhos da Tabela
oc_headers = [
    ("Nº do Pedido", 14),
    ("Empresa (GW / Fiber)", 20),
    ("Cliente", 36),
    ("Vendedor", 20),
    ("Data Faturamento", 16),
    ("Código do Material", 18),
    ("Descrição do Material", 42),
    ("Total do Item", 14),
    ("Qtd Entregue", 14),
    ("Saldo Pendente", 14),
    ("Tipo de Ocorrência", 22),
    ("Observação da Ocorrência", 50)
]

for col_idx, (h_name, width) in enumerate(oc_headers, start=1):
    cell = ws_oc.cell(row=4, column=col_idx)
    cell.value = h_name
    cell.fill = HEADER_FILL
    cell.font = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cell.border = HEADER_BORDER
    cell.protection = Protection(locked=True)
    col_letter = get_column_letter(col_idx)
    ws_oc.column_dimensions[col_letter].width = width

ws_oc.row_dimensions[4].height = 30

# Lista de Ocorrências Fornecidas pelo Usuário
user_occurrences = [
    # Pedido, SKU, Qtd Entregue, Tipo Ocorrencia, Observacao
    (637210, 18306, 22, "Furo de Estoque", "falta 8 unidades furo de estoque [Fiber - Empresa 08]"),
    (624850, 12733, 86, "Mercadoria Encontrada", "mercadoria encontrada enviar 4 restante do pedido [GW - Empresa 01]"),
    (619871, 17906, 1, "Mercadoria Encontrada", "mercadoria encontrada enviar 1 restante do pedido [Fiber - Empresa 08]"),
    (615696, 18009, 373, "Mercadoria Encontrada", "Mercadoria encontrada enviar 3 restante do pedido [Fiber - Empresa 08]"),
    (633388, 17783, 198, "Furo de Estoque", "falta 2 unidades furo de estoque [Fiber - Empresa 08]"),
    (626019, 17671, 34, "Furo de Estoque", "falta 9 unidades furo de estoque [Fiber - Empresa 08]"),
    (626019, 173, 12, "Mercadoria Encontrada", "Mercadoria encontrada enviar 1 restante do pedido [Fiber - Empresa 08]"),
    (629207, 17782, 74, "Mercadoria Encontrada", "Mercadoria encontrada enviar 6 restante do pedido [Fiber - Empresa 08]"),
    (641704, 18171, 0, "Aguardando Vendedor", "Aguardando vendedor autorizar o envio [GW - Empresa 01]"),
    (642089, 18005, 0, "Item Personalizado", "aguardando o vendedor autorizar o envio item personalizado [Fiber - Empresa 08]"),
    (631048, 17716, 0, "Item Personalizado", "Aguardando autorizar o envio item personalizado [Fiber - Empresa 08]")
]

# Obter itens do Pedido 615313 para listar os 29 itens do projeto
itens_615313 = [r for r in rows_db if r[0] == 615313]
for it in itens_615313:
    user_occurrences.append((
        615313,
        int(it[6]) if str(it[6]).isdigit() else it[6],
        0,
        "Projeto em Aprovação",
        "Projeto do cliente em aprovação aguardando vendendor autorizar o envio [GW - Empresa 01]"
    ))

current_row = 5

def apply_row_style(ws, r_num, is_zebra, status_type=None):
    base_fill = ZEBRA_FILL if is_zebra else WHITE_FILL
    for col_i in range(1, 13):
        c = ws.cell(row=r_num, column=col_i)
        c.border = THIN_BORDER
        c.font = Font(name="Segoe UI", size=9.5)
        
        # DEFINIÇÃO DE BLOQUEIO DE CÉLULAS:
        # Colunas com digitação permitida:
        # 1: Nº do Pedido
        # 6: Código do Material
        # 9: Qtd Entregue
        # 11: Tipo de Ocorrência (liberado para seleção/digitação)
        # 12: Observação da Ocorrência
        # Demais colunas (2, 3, 4, 5, 7, 8, 10): BLOQUEADAS contra edição (locked=True)
        if col_i in (1, 6, 9, 11, 12):
            c.protection = Protection(locked=False)
        else:
            c.protection = Protection(locked=True)
        
        # Alinhamentos e Formatações
        if col_i in (1, 6): # Pedido, Material (EDITÁVEL)
            c.alignment = Alignment(horizontal="center", vertical="center")
            c.number_format = "0"
            c.fill = INPUT_FILL
        elif col_i in (2, 5): # Empresa, Data (BLOQUEADO)
            c.alignment = Alignment(horizontal="center", vertical="center")
            c.fill = base_fill
        elif col_i in (3, 4, 7): # Cliente, Vendedor, Descricao (BLOQUEADO)
            c.alignment = Alignment(horizontal="left", vertical="center")
            c.fill = base_fill
        elif col_i in (8, 9, 10): # Total (BLOQ), Entregue (EDITÁVEL), Saldo (BLOQ)
            c.alignment = Alignment(horizontal="right", vertical="center")
            c.number_format = "#,##0.00"
            if col_i == 9:
                c.fill = INPUT_FILL
            else:
                c.fill = base_fill
            if col_i == 10:
                c.font = Font(name="Segoe UI", size=9.5, bold=True)
        elif col_i == 11: # Tipo Ocorrência (EDITÁVEL)
            c.alignment = Alignment(horizontal="center", vertical="center")
            if status_type and status_type in STATUS_COLORS:
                cfg = STATUS_COLORS[status_type]
                c.fill = PatternFill(start_color=cfg["fill"], end_color=cfg["fill"], fill_type="solid")
                c.font = Font(name="Segoe UI", size=9.5, bold=True, color=cfg["font"])
            else:
                c.fill = INPUT_FILL
        elif col_i == 12: # Observação (EDITÁVEL)
            c.alignment = Alignment(horizontal="left", vertical="center")
            c.fill = INPUT_FILL

# 1. Inserir Ocorrências Iniciais
for ped, mat, entregue, tipo_oc, obs in user_occurrences:
    r = current_row
    
    # Fórmulas de Busca Dinâmica
    f_empresa = f'=IF(A{r}="","",IFERROR(IF(F{r}<>"",VLOOKUP(A{r}&"_"&F{r},\'Base de Dados\'!$A:$M,5,FALSE),VLOOKUP(A{r},\'Base de Dados\'!$B:$M,4,FALSE)),"Não localizado"))'
    f_cliente = f'=IF(A{r}="","",IFERROR(IF(F{r}<>"",VLOOKUP(A{r}&"_"&F{r},\'Base de Dados\'!$A:$M,6,FALSE),VLOOKUP(A{r},\'Base de Dados\'!$B:$M,5,FALSE)),""))'
    f_vendedor = f'=IF(A{r}="","",IFERROR(IF(F{r}<>"",VLOOKUP(A{r}&"_"&F{r},\'Base de Dados\'!$A:$M,7,FALSE),VLOOKUP(A{r},\'Base de Dados\'!$B:$M,6,FALSE)),""))'
    f_data = f'=IF(A{r}="","",IFERROR(IF(F{r}<>"",VLOOKUP(A{r}&"_"&F{r},\'Base de Dados\'!$A:$M,8,FALSE),VLOOKUP(A{r},\'Base de Dados\'!$B:$M,7,FALSE)),""))'
    f_descricao = f'=IF(A{r}="","",IFERROR(IF(F{r}<>"",VLOOKUP(A{r}&"_"&F{r},\'Base de Dados\'!$A:$M,10,FALSE),VLOOKUP(A{r},\'Base de Dados\'!$B:$M,9,FALSE)),""))'
    f_total = f'=IF(A{r}="","",IFERROR(IF(F{r}<>"",VLOOKUP(A{r}&"_"&F{r},\'Base de Dados\'!$A:$M,11,FALSE),VLOOKUP(A{r},\'Base de Dados\'!$B:$M,10,FALSE)),""))'
    f_saldo = f'=IF(H{r}="","",H{r}-IF(I{r}="",0,I{r}))'

    ws_oc.cell(row=r, column=1, value=ped)
    ws_oc.cell(row=r, column=2, value=f_empresa)
    ws_oc.cell(row=r, column=3, value=f_cliente)
    ws_oc.cell(row=r, column=4, value=f_vendedor)
    ws_oc.cell(row=r, column=5, value=f_data)
    ws_oc.cell(row=r, column=6, value=mat)
    ws_oc.cell(row=r, column=7, value=f_descricao)
    ws_oc.cell(row=r, column=8, value=f_total)
    ws_oc.cell(row=r, column=9, value=entregue)
    ws_oc.cell(row=r, column=10, value=f_saldo)
    ws_oc.cell(row=r, column=11, value=tipo_oc)
    ws_oc.cell(row=r, column=12, value=obs)

    apply_row_style(ws_oc, r, (r % 2 == 0), status_type=tipo_oc)
    ws_oc.row_dimensions[r].height = 22
    current_row += 1

# 2. Inserir 100 Linhas em Branco com Fórmulas Ativas e Células Desbloqueadas para Digitação
print(f"5. Adicionando 100 linhas configuradas com fórmulas automáticas e células protegidas a partir da linha {current_row}...")
for r in range(current_row, current_row + 100):
    # Fórmulas inteligentes: se A{r} for vazio, tudo fica em branco ""
    # Se F{r} estiver vazio, F{r} puxa o primeiro SKU do pedido automaticamente
    f_mat_auto = f'=IF(A{r}="","",IFERROR(VLOOKUP(A{r},\'Base de Dados\'!$B:$M,8,FALSE),""))'
    f_empresa = f'=IF(A{r}="","",IFERROR(IF(F{r}<>"",VLOOKUP(A{r}&"_"&F{r},\'Base de Dados\'!$A:$M,5,FALSE),VLOOKUP(A{r},\'Base de Dados\'!$B:$M,4,FALSE)),"Não localizado"))'
    f_cliente = f'=IF(A{r}="","",IFERROR(IF(F{r}<>"",VLOOKUP(A{r}&"_"&F{r},\'Base de Dados\'!$A:$M,6,FALSE),VLOOKUP(A{r},\'Base de Dados\'!$B:$M,5,FALSE)),""))'
    f_vendedor = f'=IF(A{r}="","",IFERROR(IF(F{r}<>"",VLOOKUP(A{r}&"_"&F{r},\'Base de Dados\'!$A:$M,7,FALSE),VLOOKUP(A{r},\'Base de Dados\'!$B:$M,6,FALSE)),""))'
    f_data = f'=IF(A{r}="","",IFERROR(IF(F{r}<>"",VLOOKUP(A{r}&"_"&F{r},\'Base de Dados\'!$A:$M,8,FALSE),VLOOKUP(A{r},\'Base de Dados\'!$B:$M,7,FALSE)),""))'
    f_descricao = f'=IF(A{r}="","",IFERROR(IF(F{r}<>"",VLOOKUP(A{r}&"_"&F{r},\'Base de Dados\'!$A:$M,10,FALSE),VLOOKUP(A{r},\'Base de Dados\'!$B:$M,9,FALSE)),""))'
    f_total = f'=IF(A{r}="","",IFERROR(IF(F{r}<>"",VLOOKUP(A{r}&"_"&F{r},\'Base de Dados\'!$A:$M,11,FALSE),VLOOKUP(A{r},\'Base de Dados\'!$B:$M,10,FALSE)),""))'
    f_saldo = f'=IF(H{r}="","",H{r}-IF(I{r}="",0,I{r}))'

    ws_oc.cell(row=r, column=1, value="")
    ws_oc.cell(row=r, column=2, value=f_empresa)
    ws_oc.cell(row=r, column=3, value=f_cliente)
    ws_oc.cell(row=r, column=4, value=f_vendedor)
    ws_oc.cell(row=r, column=5, value=f_data)
    ws_oc.cell(row=r, column=6, value=f_mat_auto)
    ws_oc.cell(row=r, column=7, value=f_descricao)
    ws_oc.cell(row=r, column=8, value=f_total)
    ws_oc.cell(row=r, column=9, value="")
    ws_oc.cell(row=r, column=10, value=f_saldo)
    ws_oc.cell(row=r, column=11, value="")
    ws_oc.cell(row=r, column=12, value="")

    apply_row_style(ws_oc, r, (r % 2 == 0))
    ws_oc.row_dimensions[r].height = 20

# Congelar painéis abaixo do cabeçalho
ws_oc.freeze_panes = 'A5'
ws_db.freeze_panes = 'A2'

# Aplicar AutoFilter na linha 4 (cabeçalho) da aba Gestão de Ocorrências
ws_oc.auto_filter.ref = f'A4:L{ws_oc.max_row}'

# Aplicar AutoFilter na linha 1 da Base de Dados
ws_db.auto_filter.ref = f'A1:M{ws_db.max_row}'

# ATIVAR PROTEÇÃO DA PLANILHA DE OCORRÊNCIAS
# Bloqueia qualquer célula com locked=True, permitindo digitação apenas nas células com locked=False
ws_oc.protection.sheet = True
ws_oc.protection.enable()
# Permitir uso do AutoFilter e Ordenação mesmo com a planilha protegida
ws_oc.protection.autoFilter = False
ws_oc.protection.sort = False

# Garantir que a aba ativa seja "Gestão de Ocorrências"
wb.active = ws_oc

print(f"6. Salvando arquivo Excel com filtro e proteção em {excel_path}...")
wb.save(excel_path)
print("Sucesso! Planilha gerada, com filtro aplicado na linha 4 e protegida com êxito.")
