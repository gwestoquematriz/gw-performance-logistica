import os
import json

print("Loading data files...")
with open('c:/Users/renan.alves/.gemini/Projetos/Bancos/team_and_transport_data.json', encoding='utf-8') as f:
    team_data = json.load(f)

with open('c:/Users/renan.alves/.gemini/Projetos/Bancos/frota_dashboard_data.json', encoding='utf-8') as f:
    frota_data = json.load(f)

with open('c:/Users/renan.alves/.gemini/Projetos/Bancos/dashboard_data.json', encoding='utf-8') as f:
    stock_data = json.load(f)

with open('c:/Users/renan.alves/.gemini/Projetos/Bancos/reservas_furo_estoque.json', encoding='utf-8') as f:
    reservas_data = json.load(f)

print(f"Data loaded: team={len(team_data['separacao'])}, frota={len(frota_data['veiculos'])}, stock={len(stock_data['filiais'])}, reservas={len(reservas_data['reservas'])}")

# Alarmes Wisevia
alarmes_wisevia = [
    {"id": 1, "alarme": "Armazenamento de vídeo do gravador", "severidade": "Baixa", "categoria": "Equipamento"},
    {"id": 2, "alarme": "Risco de Colisão", "severidade": "Crítica", "categoria": "Segurança Viária"},
    {"id": 3, "alarme": "Vibração", "severidade": "Baixa", "categoria": "Veicular"},
    {"id": 4, "alarme": "Vídeo remoto", "severidade": "Informativa", "categoria": "Comunicação"},
    {"id": 5, "alarme": "Foto remota", "severidade": "Informativa", "categoria": "Comunicação"},
    {"id": 6, "alarme": "Calibração anormal", "severidade": "Média", "categoria": "Equipamento"},
    {"id": 7, "alarme": "Nenhum rosto detectado", "severidade": "Alta", "categoria": "Comportamento"},
    {"id": 8, "alarme": "Olhos fechados", "severidade": "Crítica", "categoria": "Fadiga"},
    {"id": 9, "alarme": "Bocejo", "severidade": "Média", "categoria": "Fadiga"},
    {"id": 10, "alarme": "Distração", "severidade": "Alta", "categoria": "Comportamento"},
    {"id": 11, "alarme": "Olhando para baixo", "severidade": "Alta", "categoria": "Comportamento"},
    {"id": 12, "alarme": "Fumando", "severidade": "Média", "categoria": "Comportamento"},
    {"id": 13, "alarme": "Uso de celular", "severidade": "Crítica", "categoria": "Comportamento"},
    {"id": 14, "alarme": "Câmera coberta", "severidade": "Crítica", "categoria": "Segurança"},
    {"id": 15, "alarme": "SOS", "severidade": "Crítica", "categoria": "Emergência"},
    {"id": 16, "alarme": "Aceleração rápida", "severidade": "Média", "categoria": "Condução"},
    {"id": 17, "alarme": "Desaceleração rápida", "severidade": "Média", "categoria": "Condução"},
    {"id": 18, "alarme": "Curva brusca", "severidade": "Média", "categoria": "Condução"},
    {"id": 19, "alarme": "Excesso de velocidade", "severidade": "Crítica", "categoria": "Condução"},
    {"id": 20, "alarme": "Cansado", "severidade": "Alta", "categoria": "Fadiga"},
    {"id": 21, "alarme": "Espaço insuficiente no cartão", "severidade": "Média", "categoria": "Equipamento"},
    {"id": 22, "alarme": "Sem cartão de memória", "severidade": "Alta", "categoria": "Equipamento"},
    {"id": 23, "alarme": "Desconexão elétrica externa", "severidade": "Crítica", "categoria": "Equipamento"},
    {"id": 24, "alarme": "Baixa voltagem", "severidade": "Média", "categoria": "Equipamento"},
    {"id": 25, "alarme": "Foto ou vídeo cronometrado", "severidade": "Informativa", "categoria": "Comunicação"},
    {"id": 26, "alarme": "RFID", "severidade": "Informativa", "categoria": "Identificação"},
    {"id": 27, "alarme": "Saída de faixa", "severidade": "Alta", "categoria": "Segurança Viária"},
    {"id": 28, "alarme": "Proximidade veículo dianteiro", "severidade": "Alta", "categoria": "Segurança Viária"},
    {"id": 29, "alarme": "Risco de colisão com pedestre", "severidade": "Crítica", "categoria": "Segurança Viária"},
    {"id": 30, "alarme": "Troca de faixa frequente", "severidade": "Média", "categoria": "Condução"},
    {"id": 31, "alarme": "Limite velocidade estrada", "severidade": "Alta", "categoria": "Condução"},
    {"id": 32, "alarme": "Obstáculo", "severidade": "Alta", "categoria": "Segurança Viária"},
    {"id": 33, "alarme": "Reconhecimento sinal estrada", "severidade": "Informativa", "categoria": "Segurança Viária"},
    {"id": 34, "alarme": "Captura ativa", "severidade": "Informativa", "categoria": "Comunicação"},
    {"id": 35, "alarme": "Fadiga", "severidade": "Crítica", "categoria": "Fadiga"},
    {"id": 36, "alarme": "Motorista não reconhecido", "severidade": "Alta", "categoria": "Identificação"},
    {"id": 37, "alarme": "Sem cinto", "severidade": "Crítica", "categoria": "Segurança"}
]

unified_data = {
    'team': team_data,
    'frota': frota_data,
    'stock': stock_data,
    'reservas': reservas_data,
    'alarmes_wisevia': alarmes_wisevia
}

with open('c:/Users/renan.alves/.gemini/Projetos/Bancos/unified_logistics_data.json', 'w', encoding='utf-8') as f:
    json.dump(unified_data, f, ensure_ascii=False)

print("unified_logistics_data.json successfully assembled!")
