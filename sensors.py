import sqlite3
import time
from datetime import datetime
try:
    import RPi.GPIO as GPIO  # Verwende echte GPIO-Bibliothek
    print("Bibliothek vorhanden!")
except ImportError:
    print("Nicht vorhanden!")
    import mockgpio as GPIO  # Fallback für Tests ohne Raspberry Pi

# GPIO-Pins (entsprechend der Sensoren)
GPIO_PINS = [2, 3, 4, 17, 27, 22, 10, 9]  # Beispiel GPIO-Pins
DB_NAME = "sensordata.db"  # Name deiner SQLite-Datenbank

# GPIO-Setup
def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    for pin in GPIO_PINS:
        GPIO.setup(pin, GPIO.IN)  # Setze die Pins als Eingänge

# Datenbank-Setup
def init_database():
    """Überprüft, ob die Tabelle 'feuchtigkeitssensoren' existiert."""
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
    """Schreibt Sensordaten in die SQLite-Datenbank."""
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

# GPIO-Zustände lesen und loggen
def read_gpio_values():
    """Liest die GPIO-Werte der 8 Pins aus."""
    return [GPIO.input(pin) for pin in GPIO_PINS]

# Hauptprogramm
def main():
    setup_gpio()
    init_database()
    print("Starte Datenerfassung. Drücke Strg+C zum Beenden.")
    try:
        sensor_values = read_gpio_values()
        print(f"Erfasste Werte: {sensor_values}")
        write_to_database(sensor_values)
    except KeyboardInterrupt:
        print("Programm beendet.")
    finally:
        GPIO.cleanup()
