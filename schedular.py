import schedule
import time
import visualize
import mail
import move
import camera
import pump
import sensors

action = ""
target_directory = "sensordata/daily/"

def sensor_check():
    print("Sensorüberprüfung läuft...")
    action = "Sensorüberprüfung"

def daily_report():
    print("Täglicher Bericht wird erstellt...")
    action = "Täglicher Bericht"

def pump():
    print("Pumpe wird gestartet...")
    time.sleep(60)  # Simuliere Pumpenlaufzeit
    action = "Pumpe"

# Aufgaben planen
schedule.every(10).seconds.do(sensors.main)  # Alle 10 Sekunden
schedule.every(30).seconds.do(camera.run)  # Jede Minute
schedule.every().day.at("19:02").do(mail.send_plant_report)  # Täglich um 18:00 Uhr
schedule.every().day.at("19:01").do(visualize.run)  # Täglich um 20:00 Uhr
schedule.every().day.at("19:03").do(lambda: move.move_files(target_directory))  # Täglich um 20:00 Uhr
schedule.every().day.at("18:52").do(pump.pump)
schedule.every().day.at("18:53").do(pump.pump)
schedule.every().day.at("18:51").do(pump.pump)

print("Scheduler gestartet...")

# Scheduler laufen lassen
while True:
    schedule.run_pending()  # Ausstehende Aufgaben ausführen
    #time.sleep(1)           # Verhindert übermäßige CPU-Auslastung
