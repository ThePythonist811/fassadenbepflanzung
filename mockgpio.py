class GPIO:
    OUT = "OUT"
    IN = "IN"

    def setmode(self, mode):
        print(f"GPIO Mode set to {mode}")

    def setup(self, pin, direction):
        print(f"Pin {pin} set to {direction}")

    def output(self, pin, state):
        print(f"Pin {pin} output set to {state}")

    def input(self, pin):
        print(f"Reading input from pin {pin}")
        return 0

    def cleanup(self):
        print("GPIO cleanup")
