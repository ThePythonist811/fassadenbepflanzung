import spidev  # SPI-Bibliothek für MCP3008
import sqlite3
from datetime import datetime
import time
import serial.tools.list_ports

DB_NAME = "sensordata/sensordata.db"

# SPI-Setup für MCP3008
spi = spidev.SpiDev()
spi.open(0, 0)  # SPI-Bus 0, Gerät 0
spi.max_speed_hz = 1350000

# GPIO- und SPI-Kanäle für die Sensoren (0–7 für 8 Kanäle)
SENSOR_CHANNELS = list(range(8))

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

# Funktion zum Auslesen eines analogen Kanals
def read_channel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

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
    try:
        while True:
            sensor_values = []
            for i, channel in enumerate(SENSOR_CHANNELS):
                raw_value = read_channel(channel)
                min_val, max_val = SENSOR_RANGES[i]
                normalized_value = normalize_value(raw_value, min_val, max_val)
                sensor_values.append(normalized_value)
            
            print(f"Erfasste Werte (normalisiert): {sensor_values}")
            write_to_database(sensor_values)
            time.sleep(1)  # Wartezeit zwischen Messungen
    except KeyboardInterrupt:
        print("Programm beendet.")
    finally:
        spi.close()

if __name__ == "__main__":
    main()
