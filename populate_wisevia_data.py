import os
import requests
import json
from datetime import datetime, timedelta
import psycopg2
from dotenv import load_dotenv

load_dotenv('c:/Users/renan.alves/.gemini/Projetos/Bancos/.env')
token = os.getenv('WISEVIA_API_TOKEN')

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}
base_url = 'https://quality.api.cloud-services.yuv.com.br'

# Mapping Plates to Branches
BRANCH_MAP = {
    'JKB3549': 'GW Matriz (Anápolis)',
    'RFQ7C99': 'GW Matriz (Anápolis)',
    'PSD1A22': 'GW Matriz (Anápolis)',
    'OVM0118': 'GW Matriz (Anápolis)',
    'EWL2976': 'GW Matriz (Anápolis)',
    'RBP9G30': 'GW Matriz (Anápolis)',
    'RMA3J97': 'GW Matriz (Anápolis)',
    'OLH8F68': 'GW Matriz (Anápolis)',
    'SDM7G76': 'GW Matriz (Anápolis)',
    'PQK8I62': 'GW Matriz (Anápolis)',
    'PRB8985': 'GW Matriz (Anápolis)',
    'SIV0J04': 'GW Matriz (Anápolis)',
    'SRK6J19': 'GW Matriz (Anápolis)',
    'RMC8I20': 'GW Matriz (Anápolis)',
    'SDB6F16': 'GW Brasília',
    'SCZ8C56': 'GW Goiânia',
    'TVD1C82': 'GW Goiânia',
    'QQK5F16': 'GW Marabá',
    'FQW9392': 'GW Marabá',
    'TVB9I73': 'GW Marabá',
    'SDB6F66': 'GW Palmas',
    'RMA9E53': 'GW São Luís'
}

print("1. Fetching available devices from Wisevia API...")
res_dev = requests.get(f'{base_url}/device/get-available', headers=headers)
devices = res_dev.json().get('data', [])
print(f"Total devices: {len(devices)}")

device_list = []
imei_list = []

for d in devices:
    parts = d.get('name', '').split(' - ')
    if len(parts) == 2:
        imei, plate = parts[0].strip(), parts[1].strip()
        filial = BRANCH_MAP.get(plate, 'GW Matriz (Anápolis)')
        device_list.append({
            'id': d.get('id'),
            'imei': imei,
            'placa': plate,
            'filial': filial
        })
        imei_list.append(imei)

# Connect to monitor_glpi and postgres
pg_conn = psycopg2.connect(
    host=os.getenv('DB_POSTGRES_HOST'),
    port=5432,
    dbname='postgres',
    user=os.getenv('DB_POSTGRES_USER'),
    password=os.getenv('DB_POSTGRES_PASSWORD')
)
pg_cur = pg_conn.cursor()

glpi_conn = psycopg2.connect(
    host=os.getenv('DB_POSTGRES_HOST'),
    port=5432,
    dbname='monitor_glpi',
    user=os.getenv('DB_POSTGRES_USER'),
    password=os.getenv('DB_POSTGRES_PASSWORD')
)
glpi_cur = glpi_conn.cursor()

print("\n2. Querying latest GPS position for each vehicle...")
veiculos_posicoes = []

for dev in device_list:
    imei = dev['imei']
    plate = dev['placa']
    filial = dev['filial']
    
    # Query GPS for recent days
    payload = {
        'deviceImei': imei,
        'startDate': '2026-08-01 00:00:00',
        'endDate': '2026-09-25 23:59:59',
        'page': 1
    }
    try:
        r = requests.get(f'{base_url}/gps', headers=headers, json=payload, timeout=12)
        if r.status_code == 200:
            data = r.json().get('data', [])
            tot = r.json().get('total', 0)
            latest = data[0] if data else None
            if latest:
                lat = float(latest.get('gpsLatitude', 0))
                lon = float(latest.get('gpsLongitude', 0))
                speed = float(latest.get('gpsSpeed', 0))
                ign = bool(int(latest.get('gpsIgnition', 0)))
                addr = latest.get('gpsAddress', '')
                time_str = latest.get('gpsTime', '')
                driver = latest.get('driverName') or dev.get('driverName', 'Motorista GW')
                
                v_obj = {
                    'placa': plate,
                    'imei': imei,
                    'filial': filial,
                    'latitude': lat,
                    'longitude': lon,
                    'velocidade': speed,
                    'ignicao': ign,
                    'endereco': addr,
                    'data_posicao': time_str,
                    'motorista': driver,
                    'total_pontos': tot,
                    'fonte': 'WISEVIA'
                }
                veiculos_posicoes.append(v_obj)
                
                # Upsert into monitor_glpi.veiculos_posicao
                glpi_cur.execute("""
                    INSERT INTO veiculos_posicao (placa, latitude, longitude, velocidade, ignicao, endereco, motorista, data_atualizacao, is_real, fonte)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (placa) DO UPDATE SET
                        latitude = EXCLUDED.latitude,
                        longitude = EXCLUDED.longitude,
                        velocidade = EXCLUDED.velocidade,
                        ignicao = EXCLUDED.ignicao,
                        endereco = EXCLUDED.endereco,
                        motorista = EXCLUDED.motorista,
                        data_atualizacao = EXCLUDED.data_atualizacao,
                        is_real = EXCLUDED.is_real,
                        fonte = EXCLUDED.fonte;
                """, (plate, lat, lon, speed, ign, addr, driver, time_str, True, 'WISEVIA'))
                
                print(f"  [OK] {plate} ({filial}) -> {time_str} | Vel: {speed} km/h | Ign: {ign} | {addr[:40]}...")
            else:
                print(f"  [WARN] {plate}: 0 pontos GPS encontrados")
        else:
            print(f"  [ERR] {plate} HTTP {r.status_code}")
    except Exception as e:
        print(f"  [ERR] {plate}: {e}")

glpi_conn.commit()
print("Updated monitor_glpi.veiculos_posicao successfully!")

print("\n3. Fetching recent Alarms from Wisevia API...")
# Fetch recent alarms
alarms_payload = {
    'deviceImeis': imei_list,
    'startDate': '2026-09-01 00:00:00',
    'endDate': '2026-09-25 23:59:59',
    'page': 1,
    'perPage': 100
}
res_alarm = requests.get(f'{base_url}/alarms', headers=headers, json=alarms_payload)
alarm_data = res_alarm.json()
total_alarms = alarm_data.get('total', 0)
recent_alarms = alarm_data.get('data', [])

print(f"Total alarms in September 2026: {total_alarms} (Fetched sample: {len(recent_alarms)})")

clean_alarms = []
for a in recent_alarms:
    plate = a.get('assetIdentifier', '')
    imei = a.get('deviceImei', '')
    filial = BRANCH_MAP.get(plate, 'GW Matriz (Anápolis)')
    alarm_name = a.get('alarmName', '')
    alarm_time = a.get('alarmTime', '')
    lat = float(a.get('alarmLatitude', 0)) if a.get('alarmLatitude') else 0.0
    lon = float(a.get('alarmLongitude', 0)) if a.get('alarmLongitude') else 0.0
    files = a.get('alarmFiles') or []
    media_url = files[0] if files else None
    driver = a.get('driverName') or 'Motorista GW'
    cust = a.get('customerName') or 'GW WIRELLES'
    
    clean_alarms.append({
        'placa': plate,
        'imei': imei,
        'filial': filial,
        'tipo_alarme': alarm_name,
        'data_hora': alarm_time,
        'latitude': lat,
        'longitude': lon,
        'motorista': driver,
        'link_midia': media_url,
        'total_midias': len(files)
    })
    
    # Insert into powerbi.fato_telemetria_wisevia
    try:
        # Convert DD/MM/YYYY HH:MM:SS to YYYY-MM-DD HH:MM:SS if needed
        dt_val = None
        if alarm_time:
            try:
                dt_val = datetime.strptime(alarm_time, '%d/%m/%Y %H:%M:%S')
            except:
                try:
                    dt_val = datetime.strptime(alarm_time, '%Y-%m-%d %H:%M:%S')
                except:
                    dt_val = None
        
        pg_cur.execute("""
            INSERT INTO powerbi.fato_telemetria_wisevia 
            (device_imei, placa, filial_nome, motorista_nome, tipo_alarme, data_hora, latitude, longitude, link_midia, cliente_nome)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (imei, plate, filial, driver, alarm_name, dt_val, lat, lon, media_url, cust))
    except Exception as e:
        pass

pg_conn.commit()
print("Saved alarms to powerbi.fato_telemetria_wisevia!")

# Save clean dataset to JSON for dashboard embedding
dataset = {
    'total_veiculos_wisevia': len(veiculos_posicoes),
    'total_alarmes_setembro': total_alarms,
    'veiculos': veiculos_posicoes,
    'alarmes_recentes': clean_alarms,
    'atualizado_em': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
}

with open('c:/Users/renan.alves/.gemini/Projetos/Bancos/wisevia_live_dataset.json', 'w', encoding='utf-8') as f:
    json.dump(dataset, f, indent=2, ensure_ascii=False)

print("\nSuccessfully generated wisevia_live_dataset.json!")

glpi_cur.close()
glpi_conn.close()
pg_cur.close()
pg_conn.close()
