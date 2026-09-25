"""
Módulo de Parametrização Oficial de Filiais (Regra de Negócio)
Mapeamento entre WMS, ERP S7 (SN) e Nomenclaturas.
"""

FILIAIS = {
    "MATRIZ": {
        "id_wms": 12,
        "nome": "GW Matriz",
        "praca": "Anápolis",
        "codigos_erp": [1, 8],
        "label": "GW Matriz (Lojas 1 e 8)"
    },
    "GOIANIA": {
        "id_wms": 9,
        "nome": "GW Filial Goiânia",
        "praca": "Goiânia",
        "codigos_erp": [6, 90],
        "label": "GW Filial Goiânia (Lojas 6 e 90)"
    },
    "BRASILIA": {
        "id_wms": 8,
        "nome": "GW Filial Brasília",
        "praca": "Brasília",
        "codigos_erp": [9, 91],
        "label": "GW Filial Brasília (Lojas 9 e 91)"
    },
    "PALMAS": {
        "id_wms": 11,
        "nome": "GW Filial Palmas",
        "praca": "Palmas",
        "codigos_erp": [10, 11],
        "label": "GW Filial Palmas (Lojas 10 e 11)"
    },
    "MARABA": {
        "id_wms": 10,
        "nome": "GW Filial Marabá",
        "praca": "Marabá",
        "codigos_erp": [7, 92],
        "label": "GW Filial Marabá (Lojas 7 e 92)"
    },
    "SAO_LUIS": {
        "id_wms": 7,
        "nome": "GW Filial São Luís",
        "praca": "São Luís",
        "codigos_erp": [14],
        "label": "GW Filial São Luís (Loja 14)"
    }
}

def get_filial_por_codigo_erp(codigo):
    for chave, f in FILIAIS.items():
        if codigo in f["codigos_erp"]:
            return f
    return None

def get_filial_por_id_wms(id_wms):
    for chave, f in FILIAIS.items():
        if f["id_wms"] == id_wms:
            return f
    return None
