import serial.tools.list_ports
import sqlite3
from datetime import datetime
import time

DB_NAME = "sensordata.db"

# Individuelle Messbereiche der Sensoren (min, max) in einer Liste
SENSOR_RANGES = [
    (0, 500),  # Sensor 1
    (50, 600),  # Sensor 2
    (100, 670),  # Sensor 3
    (30, 550),  # Sensor 4
    (10, 670),  # Sensor 5
    (0, 400),  # Sensor 6
    (20, 650),  # Sensor 7
    (5, 620)    # Sensor 8
]

# Normalisierung der Sensorwerte (auf 0–100% basierend auf individuelle Bereiche)
def normalize_value(value, min_value, max_value):
    return round(((value - min_value) / (max_value - min_value)) * 100, 2)

# Datenbank-Setup
def init_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feuchtigkeitssensoren (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            sensor_1 REAL,
            sensor_2 REAL,
            sensor_3 REAL,
            sensor_4 REAL,
            sensor_5 REAL,
            sensor_6 REAL,
            sensor_7 REAL,
            sensor_8 REAL
        )
    """)
    conn.commit()
    conn.close()

# Daten in die Datenbank schreiben
def write_to_database(sensor_values):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO feuchtigkeitssensoren (
            timestamp, sensor_1, sensor_2, sensor_3, sensor_4,
            sensor_5, sensor_6, sensor_7, sensor_8
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (timestamp, *sensor_values))
    conn.commit()
    conn.close()

# Hauptprogramm
def main():
    init_database()
    print("Starte Datenerfassung...")

    # Standard-Serial-Port
    serial_port = "/dev/ttyACM0"
    try:
        serial_connection = serial.Serial(serial_port, baudrate=9600, timeout=1)
        print(f"Verbindung zu {serial_port} erfolgreich hergestellt!")
    except serial.SerialException as e:
        print(f"Fehler beim Öffnen des Ports {serial_port}: {e}")
        return

    try:
        while True:
            if serial_connection.in_waiting > 0:
                try:
                    # Datenpaket vom Serial-Port lesen
                    packet = serial_connection.readline().strip()

                    # Debug-Ausgabe
                    print(f"Empfangene Daten: {packet}")

                    # Dekodiere empfangene Daten als Integer-Liste
                    decoded_packet = packet.decode('ascii', errors='ignore')
                    raw_values = list(map(int, decoded_packet.split(',')))

                    # Überprüfen, ob die Anzahl der empfangenen Werte korrekt ist
                    if len(raw_values) != len(SENSOR_RANGES):
                        print(f"Fehler: Ungültige Anzahl von Sensorwerten empfangen (Erwartet: {len(SENSOR_RANGES)}, Empfangen: {len(raw_values)})")
                        continue

                    # Werte normalisieren
                    sensor_values = [
                        normalize_value(raw_value, min_val, max_val)
                        for raw_value, (min_val, max_val) in zip(raw_values, SENSOR_RANGES)
                    ]

                    print(f"Erfasste Werte (normalisiert): {sensor_values}")
                    write_to_database(sensor_values)

                except ValueError:
                    print("Fehler: Ungültige Daten empfangen.")

            time.sleep(1)  # Wartezeit zwischen Messungen

    except KeyboardInterrupt:
        print("Programm beendet.")
    finally:
        serial_connection.close()

if __name__ == "__main__":
    main()
