import os
import re
import html
import pymysql
from dotenv import load_dotenv

load_dotenv('c:/Users/renan.alves/.gemini/Projetos/Bancos/.env')

glpi_conn = pymysql.connect(
    host=os.getenv('DB_GLPI_HOST'),
    port=int(os.getenv('DB_GLPI_PORT', 3306)),
    user=os.getenv('DB_GLPI_USER'),
    password=os.getenv('DB_GLPI_PASSWORD'),
    database=os.getenv('DB_GLPI_DATABASE', 'glpidb'),
    charset='utf8mb4'
)
gcur = glpi_conn.cursor()

# Find tickets where content has "Tipo de Pagamento" or "Veículo"
gcur.execute("""
    SELECT id, name, date, status, content 
    FROM glpi_tickets 
    WHERE (content LIKE '%Pagamento%' OR content LIKE '%Placa%')
      AND (content LIKE '%Ve%culo%' OR content LIKE '%Manuten%')
      AND is_deleted = 0
    ORDER BY id DESC LIMIT 500;
""")
tickets = gcur.fetchall()
print(f"Total tickets avaliados: {len(tickets)}")

def parse_glpi_form(content):
    data = {}
    if not content:
        return data
    decoded = html.unescape(content)
    # Match patterns like <b>1) Tipo de Pagamento : </b>VALOR</div>
    matches = re.findall(r'<b[^>]*>(?:(?:\d+[\)\.\-]\s*)?([^:<]+))\s*:\s*</b>\s*([^<]+)', decoded)
    for k, v in matches:
        k_clean = k.strip().upper()
        v_clean = v.strip()
        data[k_clean] = v_clean
    return data

manutencao_tickets = []
for t in tickets:
    form = parse_glpi_form(t[4])
    tipo_pag = form.get('TIPO DE PAGAMENTO', '').upper()
    placa = form.get('PLACA', '').upper().replace('-', '').strip()
    veiculo = form.get('VEÍCULO', form.get('VEICULO', ''))
    if 'MANUTEN' in tipo_pag or placa or 'OFICINA' in tipo_pag or 'PEÇAS' in tipo_pag:
        manutencao_tickets.append({
            'id': t[0],
            'titulo': t[1],
            'data': str(t[2]),
            'status': t[3],
            'tipo_pagamento': tipo_pag,
            'placa': placa,
            'veiculo': veiculo,
            'fornecedor': form.get('NOME DO FORNECEDOR', ''),
            'valor': form.get('VALOR', form.get('VALOR DO PEDIDO', '')),
            'finalidade': form.get('FINALIDADE', ''),
            'localidade': form.get('LOCALIDADE', '')
        })

print(f"Total tickets de MANUTENÇÃO DE VEÍCULOS extraídos: {len(manutencao_tickets)}")
print("\nPrimeiros 5 tickets extraídos com sucesso do GLPI:")
for m in manutencao_tickets[:5]:
    print(m)

gcur.close()
glpi_conn.close()
