HIGH = 1
LOW = 0
BCM = "BCM"
OUT = "OUT"  # Ausgangsmodus hinzufügen
IN = "IN"    # Optional: Eingangsmodus hinzufügen

def setmode(mode):
    print(f"GPIO Mode set to {mode}")

def setup(pin, direction):
    print(f"Setup Pin {pin} as {direction}")

def output(pin, state):
    print(f"Set Pin {pin} to {'HIGH' if state == HIGH else 'LOW'}")

def cleanup():
    print("GPIO cleanup complete")
