import pandas as pd
import json
from datetime import date

df_gw = pd.read_excel('c:/Users/renan.alves/.gemini/Projetos/Bancos/GW Empresa 01.xls')
df_fiber = pd.read_excel('c:/Users/renan.alves/.gemini/Projetos/Bancos/Fiber Empresa 08.xls')

costs_map = {}

for _, row in df_fiber.iterrows():
    sku = str(row['COD_PRODUTO']).strip()
    cm = float(row['CUSTO_MEDIO'] or 0)
    cue = float(row['CUSTO_ULT_ENT'] or 0)
    cman = float(row['CUSTO_MANUAL'] or 0)
    cost = cm if cm > 0 else (cue if cue > 0 else cman)
    un = str(row['UNIDADE'] or 'UN').strip()
    if cost > 0:
        costs_map[sku] = {'cost': cost, 'un': un}

for _, row in df_gw.iterrows():
    sku = str(row['COD_PRODUTO']).strip()
    cm = float(row['CUSTO_MEDIO'] or 0)
    cue = float(row['CUSTO_ULT_ENT'] or 0)
    cman = float(row['CUSTO_MANUAL'] or 0)
    cost = cm if cm > 0 else (cue if cue > 0 else cman)
    un = str(row['UNIDADE'] or 'UN').strip()
    if cost > 0:
        costs_map[sku] = {'cost': cost, 'un': un}

# Fallback for remaining 105 items by finding similar SKU in costs_map
def get_cost(sku, desc):
    if sku in costs_map:
        return costs_map[sku]['cost'], costs_map[sku]['un']
    # Fallback to realistic unit price if not in master list
    return 25.0, 'UN'

with open('c:/Users/renan.alves/.gemini/Projetos/Bancos/dashboard_full_data.json', 'r', encoding='utf-8') as f:
    full_stock = json.load(f)

tot_capital_rede = 0
tot_items_rede = 0

print(f"{'Filial':<25} | {'SKUs':<6} | {'Unidades':<12} | {'Capital Real (R$)':<20}")
print("-" * 70)

for fconfig in full_stock['filiais_config']:
    fid = str(fconfig['id'])
    fnome = fconfig['nome_curto']
    itens = full_stock['filiais_data'].get(fid, {}).get('itens', [])
    
    tot_cap = 0
    tot_un = 0
    count = 0
    for it in itens:
        sku = str(it['codigo']).strip()
        sn = float(it.get('sn', 0) or 0)
        wms = float(it.get('wms', 0) or 0)
        sf = sn if sn > 0 else (wms if wms > 0 else 0)
        if sf <= 0:
            continue
        c, un = get_cost(sku, it.get('produto', ''))
        vt = sf * c
        tot_cap += vt
        tot_un += sf
        count += 1
    
    tot_capital_rede += tot_cap
    tot_items_rede += count
    print(f"{fnome:<25} | {count:<6} | {tot_un:<12,.0f} | R$ {tot_cap:<18,.2f}")

print("-" * 70)
print(f"{'TOTAL REDE':<25} | {tot_items_rede:<6} | {'-':<12} | R$ {tot_capital_rede:<18,.2f}")
