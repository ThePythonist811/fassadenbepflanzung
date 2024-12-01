import shutil
import os
from datetime import datetime

def move_files(target_directory):
    # Aktuelles Datum im Format YYYY-MM-DD
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Liste der zu verschiebenden Dateien
    source_files = [
        f"{today}_sensor_comparison.png",
        f"{today}_sensordaten.xlsx"
    ]
    
    # Überprüfen, ob das Zielverzeichnis existiert, falls nicht, erstellen
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    # Dateien verschieben
    for file in source_files:
        try:
            # Überprüfen, ob die Datei existiert
            if os.path.exists(file):
                # Zielpfad für die Datei erstellen
                target_file = os.path.join(target_directory, os.path.basename(file))
                # Datei verschieben
                shutil.move(file, target_file)
                print(f"Datei {file} wurde nach {target_file} verschoben.")
            else:
                print(f"Datei {file} existiert nicht.")
        except Exception as e:
            print(f"Fehler beim Verschieben der Datei {file}: {e}")