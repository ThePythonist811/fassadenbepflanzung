# Definiere die Zustände für die Pins
HIGH = 1
LOW = 0
BCM = "BCM"
OUT = "OUT"  # Ausgangsmodus
IN = "IN"    # Eingangsmodus

# Ein Dictionary, das den Zustand jedes Pins speichert
PIN_STATE = {}

def setmode(mode):
    print(f"GPIO Mode set to {mode}")

def setup(pin, direction):
    """Konfiguriere einen Pin als Eingang oder Ausgang."""
    PIN_STATE[pin] = {'mode': direction, 'state': LOW}  # Standardmäßig LOW für den Zustand
    print(f"Setup Pin {pin} as {direction}")

def output(pin, state):
    """Setze den Zustand eines Ausgangspins."""
    if pin in PIN_STATE and PIN_STATE[pin]['mode'] == OUT:
        PIN_STATE[pin]['state'] = state
        print(f"Set Pin {pin} to {'HIGH' if state == HIGH else 'LOW'}")
    else:
        print(f"Pin {pin} is not set as output.")

def input(pin):
    """Lese den Zustand eines Eingangspins."""
    if pin in PIN_STATE and PIN_STATE[pin]['mode'] == IN:
        return PIN_STATE[pin]['state']
    else:
        print(f"Pin {pin} is not set as input.")
        return None

def cleanup():
    """Führe eine Aufräumfunktion aus, wenn die GPIOs nicht mehr benötigt werden."""
    print("GPIO cleanup complete")