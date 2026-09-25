import os
import requests
import json
from dotenv import load_dotenv

load_dotenv('c:/Users/renan.alves/.gemini/Projetos/Bancos/.env')
token = os.getenv('WISEVIA_API_TOKEN')

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

base_url = 'https://quality.api.cloud-services.yuv.com.br'

imeis = [
    '864993060191286', '864993060189314', '864993060176766', '864993060187813',
    '864993060257095', '869247060361257', '864993060179687', '864993060257640',
    '864993060149888', '864993060187490', '864993060142248', '864993060185635',
    '869247060359574'
]

# 1. Check Alarms in September 2026
payload_sept = {
    'deviceImeis': imeis,
    'startDate': '2026-09-01 00:00:00',
    'endDate': '2026-09-25 23:59:59',
    'page': 1,
    'perPage': 100
}

res = requests.get(f'{base_url}/alarms', headers=headers, json=payload_sept)
data = res.json()
print("Alarms in Sept 2026:", data.get('total', 0))
if data.get('data'):
    for a in data.get('data')[:10]:
        files_count = len(a.get('alarmFiles') or [])
        print(f"  {a.get('assetIdentifier')} | {a.get('alarmTime')} | {a.get('alarmName')} | Loc: {a.get('alarmLatitude')}, {a.get('alarmLongitude')} | Midias: {files_count}")

# 2. Check Alarms in August 2026
payload_aug = {
    'deviceImeis': imeis,
    'startDate': '2026-08-01 00:00:00',
    'endDate': '2026-08-31 23:59:59',
    'page': 1,
    'perPage': 100
}
res_aug = requests.get(f'{base_url}/alarms', headers=headers, json=payload_aug)
data_aug = res_aug.json()
print("\nAlarms in Aug 2026:", data_aug.get('total', 0))
if data_aug.get('data'):
    for a in data_aug.get('data')[:10]:
        files_count = len(a.get('alarmFiles') or [])
        print(f"  {a.get('assetIdentifier')} | {a.get('alarmTime')} | {a.get('alarmName')} | Loc: {a.get('alarmLatitude')}, {a.get('alarmLongitude')} | Midias: {files_count}")


print("\n================ FULL GPS SCAN FOR ALL WISEVIA VEHICLES ================")
res_dev = requests.get(f'{base_url}/device/get-available', headers=headers)
devices = res_dev.json().get('data', [])

for d in devices:
    parts = d.get('name', '').split(' - ')
    if len(parts) == 2:
        imei, plate = parts[0].strip(), parts[1].strip()
        payload = {
            'deviceImei': imei,
            'startDate': '2026-08-01 00:00:00',
            'endDate': '2026-09-25 23:59:59',
            'page': 1
        }
        r = requests.get(f'{base_url}/gps', headers=headers, json=payload)
        if r.status_code == 200:
            pts = r.json().get('data', [])
            tot = r.json().get('total', 0)
            latest = pts[0] if pts else None
            if latest:
                time_str = latest.get('gpsTime')
                speed = latest.get('gpsSpeed')
                ign = latest.get('gpsIgnition')
                addr = latest.get('gpsAddress')
                lat = latest.get('gpsLatitude')
                lon = latest.get('gpsLongitude')
                print(f"[{plate}] IMEI {imei} | {tot} pts | {time_str} | Vel: {speed} km/h | Ign: {ign} | Lat: {lat}, Lon: {lon} | {addr}")
            else:
                print(f"[{plate}] IMEI {imei} | 0 pts no período")
        else:
            print(f"[{plate}] IMEI {imei} | HTTP {r.status_code}")

