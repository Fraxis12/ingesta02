import boto3
import mysql.connector
import csv
import os

# ── Configuración MySQL ──────────────────────────
DB_HOST     = os.environ.get("DB_HOST", "75.101.242.126")  # IP 
DB_USER     = os.environ.get("DB_USER", "ingesta_user")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "123456")
DB_NAME     = os.environ.get("DB_NAME", "testdb")
DB_TABLE    = os.environ.get("DB_TABLE", "clientes")

# ── Configuración S3 ─────────────────────────────
BUCKET_NAME  = "tareaaa"          # ← cambia por tu bucket
CSV_FILENAME = "data_mysql.csv"

# ── 1. Leer datos desde MySQL ────────────────────
print("Conectando a MySQL...")
conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)
cursor = conn.cursor()
cursor.execute(f"SELECT * FROM {DB_TABLE}")
rows    = cursor.fetchall()
headers = [desc[0] for desc in cursor.description]
cursor.close()
conn.close()
print(f"Registros leídos: {len(rows)}")

# ── 2. Guardar en CSV ────────────────────────────
with open(CSV_FILENAME, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(rows)
print(f"Archivo CSV creado: {CSV_FILENAME}")

# ── 3. Subir CSV a S3 ────────────────────────────
print(f"Subiendo a S3 bucket: {BUCKET_NAME}")
s3 = boto3.client("s3")
s3.upload_file(CSV_FILENAME, BUCKET_NAME, CSV_FILENAME)
print("Ingesta completada")
