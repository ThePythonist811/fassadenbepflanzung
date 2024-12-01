import sqlite3
from datetime import datetime

# Verbindung zur Datenbank herstellen
connection = sqlite3.connect("/home/findus/Organisation/pflanzen2/sensordata/sensordata.db")
cursor = connection.cursor()

# Tabelle erstellen (falls nicht vorhanden)
cursor.execute("""
CREATE TABLE IF NOT EXISTS feuchtigkeitssensoren (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    sensor_1 REAL NOT NULL,
    sensor_2 REAL NOT NULL,
    sensor_3 REAL NOT NULL,
    sensor_4 REAL NOT NULL,
    sensor_5 REAL NOT NULL,
    sensor_6 REAL NOT NULL,
    sensor_7 REAL NOT NULL,
    sensor_8 REAL NOT NULL
)
""")

def speichere_daten(sensorwerte):
    cursor.execute("""
    INSERT INTO feuchtigkeitssensoren (sensor_1, sensor_2, sensor_3, sensor_4,
                                       sensor_5, sensor_6, sensor_7, sensor_8)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, sensorwerte)
    connection.commit()

# Beispiel-Daten einfügen
sensorwerte = [45.3, 50.2, 49.8, 55.0, 60.3, 47.9, 53.1, 52.0]  # Simulierte Werte
speichere_daten(sensorwerte)


connection.commit()
