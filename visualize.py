import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# 1. Verbindung zur SQLite-Datenbank herstellen
db_path = "sensordata/sensordata.db"  # Pfad zur Datenbank
connection = sqlite3.connect(db_path)

# 2. Daten des aktuellen Tages abrufen
def hole_daten():
    heute = datetime.now().strftime("%Y-%m-%d")  # Aktuelles Datum
    query = f"""
    SELECT timestamp, sensor_1, sensor_2, sensor_3, sensor_4, 
           sensor_5, sensor_6, sensor_7, sensor_8
    FROM feuchtigkeitssensoren
    WHERE DATE(timestamp) = '{heute}'
    """
    return pd.read_sql_query(query, connection)

# 3. Daten in eine Excel-Datei speichern
def speichere_excel(daten):
    heute = datetime.now().strftime("%Y-%m-%d")  # Aktuelles Datum
    dateiname = f"{heute}_sensordaten.xlsx"  # Dynamischer Dateiname
    daten.to_excel(dateiname, index=False, engine="openpyxl")
    print(f"Daten wurden in {dateiname} gespeichert.")

# 4. Graphen erstellen (Vergleich der Untergründe)
def erstelle_graph(daten):
    # Sensoren zu Untergründen gruppieren
    untergruende = {
        "Steinwolle": ["sensor_1", "sensor_2"],
        "Silicagel": ["sensor_3", "sensor_4"],
        "Tonkugeln": ["sensor_5", "sensor_6"],
        "Schaumstoff": ["sensor_7", "sensor_8"]
    }
    
    # Durchschnittswerte für jeden Untergrund berechnen
    mittelwerte = {key: daten[sensoren].mean(axis=1) for key, sensoren in untergruende.items()}

    # Graph plotten
    plt.figure(figsize=(10, 6))
    for untergrund, werte in mittelwerte.items():
        plt.plot(daten['timestamp'], werte, label=untergrund)
    
    plt.title("Feuchtigkeitsvergleich zwischen Untergründen")
    plt.xlabel("Zeit")
    plt.ylabel("Feuchtigkeit (%)")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Dynamischer Graph-Name
    heute = datetime.now().strftime("%Y-%m-%d")
    graph_name = f"{heute}_sensor_comparison.png"
    plt.savefig(graph_name)  # Speichern des Graphen als Bild
    plt.show()
    print(f"Graph wurde als {graph_name} gespeichert.")


def run():
    # Hauptprogramm
    daten = hole_daten()
    if not daten.empty:
        speichere_excel(daten)          # Daten in Excel speichern
        erstelle_graph(daten)          # Graph erstellen
    else:
        print("Keine Daten für den aktuellen Tag gefunden.")

    # Verbindung schließen
    connection.close()
