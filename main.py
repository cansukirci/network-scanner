import sqlite3
import ast
import csv
import ipaddress

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from scanner import scan_network

from database import (
    create_table,
    save_device,
    reset_last_seen,
    save_last_scan,
    get_last_scan
)


app = FastAPI()

create_table()


# --------------------------------------------------
# TARAMA İSTEĞİNİN MODELİ
# --------------------------------------------------

class ScanRequest(BaseModel):
    ip_range: str


# --------------------------------------------------
# SQLite satırını cihaz sözlüğüne dönüştürür
# --------------------------------------------------

def row_to_device(row):
    return {
        "id": row[0],
        "ip": row[1],
        "mac": row[2],
        "hostname": row[3],
        "open_ports": ast.literal_eval(row[4]),
        "last_seen": row[5]
    }


# --------------------------------------------------
# ANA SAYFA
# --------------------------------------------------

@app.get("/")
def home():
    return FileResponse("index.html")


# --------------------------------------------------
# TÜM CİHAZLARI GETİR
# --------------------------------------------------

@app.get("/devices")
def get_devices():

    connection = sqlite3.connect("network.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM devices")
    rows = cursor.fetchall()

    connection.close()

    devices = []

    for row in rows:
        devices.append(row_to_device(row))

    return devices


# --------------------------------------------------
# SON TARAMA ZAMANINI GETİR
# --------------------------------------------------

@app.get("/last-scan")
def last_scan():

    return {
        "last_scan": get_last_scan()
    }


# --------------------------------------------------
# CSV DIŞA AKTARMA
# --------------------------------------------------

@app.get("/export")
def export_devices():

    connection = sqlite3.connect("network.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM devices")
    rows = cursor.fetchall()

    connection.close()

    file_name = "devices.csv"

    with open(
        file_name,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "ID",
            "IP",
            "MAC",
            "Hostname",
            "Acik Portlar",
            "Durum"
        ])

        for row in rows:

            status = "Aktif" if row[5] == 1 else "Pasif"

            writer.writerow([
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                status
            ])

    return FileResponse(
        file_name,
        media_type="text/csv",
        filename="devices.csv"
    )


# --------------------------------------------------
# IP ADRESİNE GÖRE CİHAZ GETİR
# --------------------------------------------------

@app.get("/devices/ip/{ip_address}")
def get_device_by_ip(ip_address: str):

    connection = sqlite3.connect("network.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM devices WHERE ip = ?",
        (ip_address,)
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Bu IP adresine ait cihaz bulunamadı"
        )

    return row_to_device(row)


# --------------------------------------------------
# ID İLE TEK CİHAZ GETİR
# --------------------------------------------------

@app.get("/devices/{device_id}")
def get_device(device_id: int):

    connection = sqlite3.connect("network.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM devices WHERE id = ?",
        (device_id,)
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Cihaz bulunamadı"
        )

    return row_to_device(row)


# --------------------------------------------------
# AĞ TARAMASI
# --------------------------------------------------

@app.post("/scan")
def run_scan(request: ScanRequest):

    ip_range = request.ip_range.strip()

    # IP/CIDR kontrolü
    try:
        network = ipaddress.ip_network(
            ip_range,
            strict=False
        )

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Geçersiz IP aralığı. Örnek: 192.168.1.0/24"
        )

    # Bu proje IPv4 tarıyor
    if network.version != 4:
        raise HTTPException(
            status_code=400,
            detail="Şimdilik yalnızca IPv4 ağları destekleniyor."
        )

    # Çok büyük ağların yanlışlıkla taranmasını engelle
    if network.num_addresses > 256:
        raise HTTPException(
            status_code=400,
            detail="En fazla /24 büyüklüğünde bir ağ tarayabilirsiniz."
        )

    # Doğrulanmış ağ adresini kullan
    ip_range = str(network)

    reset_last_seen()

    devices = scan_network(ip_range)

    for device in devices:

        save_device(
            device["ip"],
            device["mac"],
            device["hostname"],
            device["open_ports"]
        )

    save_last_scan()

    return {
        "message": "Tarama tamamlandı",
        "ip_range": ip_range,
        "device_count": len(devices),
        "devices": devices
    }