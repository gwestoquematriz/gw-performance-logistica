import os
import psycopg2
import pymysql
from dotenv import load_dotenv

load_dotenv('c:/Users/renan.alves/.gemini/Projetos/Bancos/.env')

print("--- 1. GLPI: Tickets de Manutenção de Veículos ---")
glpi_conn = pymysql.connect(
    host=os.getenv('DB_GLPI_HOST'),
    port=int(os.getenv('DB_GLPI_PORT', 3306)),
    user=os.getenv('DB_GLPI_USER'),
    password=os.getenv('DB_GLPI_PASSWORD'),
    database=os.getenv('DB_GLPI_DATABASE', 'glpidb'),
    charset='utf8mb4'
)
gcur = glpi_conn.cursor()

# Categories in GLPI
gcur.execute("""
    SELECT id, name, completename 
    FROM glpi_itilcategories 
    WHERE name LIKE '%manut%' OR name LIKE '%veic%' OR name LIKE '%frota%' OR name LIKE '%transp%'
    ORDER BY name;
""")
print("Categorias GLPI relacionadas a manutencao/frota:")
for r in gcur.fetchall():
    print(r)

# Tickets mentioning manutencao, veiculo, placa, oficina
gcur.execute("""
    SELECT t.id, t.name, t.date, t.status, it.name as categoria, t.content
    FROM glpi_tickets t
    LEFT JOIN glpi_itilcategories it ON t.itilcategories_id = it.id
    WHERE (t.name LIKE '%manut%' OR t.name LIKE '%veic%' OR t.name LIKE '%troca%' OR t.name LIKE '%pneu%' OR t.name LIKE '%oficina%' OR t.name LIKE '%revisao%'
           OR it.name LIKE '%manut%' OR it.name LIKE '%veic%')
      AND t.is_deleted = 0
    ORDER BY t.id DESC LIMIT 10;
""")
print("\nUltimos chamados de manutencao no GLPI:")
for r in gcur.fetchall():
    print(r[0], r[1], r[2], r[3], r[4], (r[5][:80] if r[5] else ''))

gcur.close()
glpi_conn.close()

print("\n--- 2. PostgreSQL: Sistema de Programação / Romaneios do Gabriel Joffre ---")
pg_conn = psycopg2.connect(
    host=os.getenv('DB_POSTGRES_HOST'),
    port=os.getenv('DB_POSTGRES_PORT', 5432),
    dbname=os.getenv('DB_POSTGRES_DATABASE', 'postgres'),
    user=os.getenv('DB_POSTGRES_USER'),
    password=os.getenv('DB_POSTGRES_PASSWORD')
)
cur = pg_conn.cursor()

# Check romaneios columns
cur.execute("""
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_schema = 'gw_fdw' AND table_name = 'romaneios'
    ORDER BY ordinal_position;
""")
print("gw_fdw.romaneios columns:")
for r in cur.fetchall():
    print(r)

# Check sample romaneios
cur.execute("""
    SELECT * FROM gw_fdw.romaneios ORDER BY id DESC LIMIT 3;
""")
print("\nSample romaneios:")
for r in cur.fetchall():
    print(r)

# Check motoristas_localizacao
cur.execute("""
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_schema = 'gw_fdw' AND table_name = 'motoristas_localizacao'
    ORDER BY ordinal_position;
""")
print("\ngw_fdw.motoristas_localizacao columns:")
for r in cur.fetchall():
    print(r)

cur.execute("""
    SELECT * FROM gw_fdw.motoristas_localizacao ORDER BY id DESC LIMIT 3;
""")
print("\nSample motoristas_localizacao:")
for r in cur.fetchall():
    print(r)

cur.close()
pg_conn.close()
