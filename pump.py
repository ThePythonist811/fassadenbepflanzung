#import RPi.GPIO as GPIO
import mock_gpio as GPIO
import time

PIN = 18

# GPIO-Modus und Pin einrichten
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT)

try:
    GPIO.output(PIN, GPIO.HIGH)
    print(f"Pin {PIN} ist eingeschaltet.")
    time.sleep(60)
except:
    print("ERROR!")
finally:
    GPIO.cleanup()
    print(f"Pin {PIN} zurückgesetzt.")