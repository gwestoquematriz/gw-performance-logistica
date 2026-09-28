import re
import json

with open('c:/Users/renan.alves/.gemini/Projetos/Bancos/Dashboard_Performance_Operacional_Logistico.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Check DATA JSON
start = html.find('const DATA = ') + len('const DATA = ')
end = html.find(';\n', start)
try:
    d = json.loads(html[start:end])
    print("DATA keys:", list(d.keys()))
    print("Estoque parado keys:", list(d['estoque_parado'].keys()))
    print(f"Estoque parado total items: {len(d['estoque_parado']['itens'])}")
    print("Sample item 0:", d['estoque_parado']['itens'][0])
except Exception as e:
    print("DATA JSON error:", e)

# 2. Check IDs
expected_ids = [
    'view-hub', 'view-performance', 'view-acuracidade', 'view-transporte',
    'btn-acur-sem-giro', 'acur-sem-giro', 'kpi-parado-valor', 'kpi-parado-skus',
    'search-parado', 'btn-period-90', 'btn-period-all', 'input-custom-days',
    'input-custom-date', 'sort-parado', 'tbody-estoque-parado', 'section-action-plan'
]
print("\nChecking expected IDs in HTML:")
all_ok = True
for eid in expected_ids:
    found = f'id="{eid}"' in html
    print(f"  {eid}: {'FOUND' if found else 'MISSING'}")
    if not found:
        all_ok = False

# 3. Check functions
expected_funcs = [
    'renderEstoqueParado', 'renderTableEstoqueParado', 'getFilteredEstoqueParadoList',
    'setParadoPeriod', 'setCustomDays', 'setCustomDate',
    'exportEstoqueParadoExcel', 'switchAcuracidadeTab', 'applyAcuracidadeFilters'
]
print("\nChecking expected functions in HTML:")
for fn in expected_funcs:
    found = f'function {fn}' in html
    print(f"  {fn}: {'FOUND' if found else 'MISSING'}")
    if not found:
        all_ok = False

print("\nINTEGRITY STATUS:", "ALL CHECKS PASSED!" if all_ok else "ERRORS FOUND!")
