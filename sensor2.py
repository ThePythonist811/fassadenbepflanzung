import RPi.GPIO as GPIO
from datetime import datetime
import sqlite3
import time

# GPIO-Pins der digitalen Sensoren
GPIO_PINS = [2, 3, 4, 17, 27, 22, 10, 9]  # Pins für 8 Sensoren
DB_NAME = "sensordata/sensordata.db"

# GPIO-Setup
def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    for pin in GPIO_PINS:
        GPIO.setup(pin, GPIO.IN)

# Digitale Werte lesen
def read_digital_sensors():
    return [GPIO.input(pin) for pin in GPIO_PINS]

# Datenbank-Setup
def init_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feuchtigkeitssensoren (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            sensor_1 INTEGER,
            sensor_2 INTEGER,
            sensor_3 INTEGER,
            sensor_4 INTEGER,
            sensor_5 INTEGER,
            sensor_6 INTEGER,
            sensor_7 INTEGER,
            sensor_8 INTEGER
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
    setup_gpio()
    init_database()
    print("Starte Datenerfassung...")
    try:
        while True:
            sensor_values = read_digital_sensors()
            print(f"Erfasste Werte: {sensor_values}")
            write_to_database(sensor_values)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Programm beendet.")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
