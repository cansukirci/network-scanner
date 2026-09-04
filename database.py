import sqlite3
from datetime import datetime


def create_table():
    connection = sqlite3.connect("network.db")
    cursor = connection.cursor()

    # Cihaz tablosu
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS devices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT,
        mac TEXT,
        hostname TEXT,
        open_ports TEXT,
        last_seen INTEGER DEFAULT 0
    )
    """)

    # Tarama bilgilerini tutan tablo
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scan_info (
        id INTEGER PRIMARY KEY,
        last_scan TEXT
    )
    """)

    connection.commit()
    connection.close()


def reset_last_seen():
    connection = sqlite3.connect("network.db")
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE devices
    SET last_seen = 0
    """)

    connection.commit()
    connection.close()


def save_device(ip, mac, hostname, open_ports):
    connection = sqlite3.connect("network.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id FROM devices WHERE mac = ?",
        (mac,)
    )

    existing_device = cursor.fetchone()

    if existing_device:
        cursor.execute("""
        UPDATE devices
        SET ip = ?, hostname = ?, open_ports = ?, last_seen = 1
        WHERE mac = ?
        """, (
            ip,
            hostname,
            str(open_ports),
            mac
        ))

    else:
        cursor.execute("""
        INSERT INTO devices (
            ip,
            mac,
            hostname,
            open_ports,
            last_seen
        )
        VALUES (?, ?, ?, ?, ?)
        """, (
            ip,
            mac,
            hostname,
            str(open_ports),
            1
        ))

    connection.commit()
    connection.close()


def save_last_scan():
    connection = sqlite3.connect("network.db")
    cursor = connection.cursor()

    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    cursor.execute("""
    INSERT OR REPLACE INTO scan_info (id, last_scan)
    VALUES (1, ?)
    """, (now,))

    connection.commit()
    connection.close()


def get_last_scan():
    connection = sqlite3.connect("network.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT last_scan
    FROM scan_info
    WHERE id = 1
    """)

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return row[0]


if __name__ == "__main__":
    create_table()
    print("Veritabanı hazır.")