class GPIO:
    HIGH = 1
    LOW = 0
    BCM = "BCM"

    @staticmethod
    def setmode(mode):
        print(f"GPIO Mode set to {mode}")

    @staticmethod
    def setup(pin, direction):
        print(f"Setup Pin {pin} as {direction}")

    @staticmethod
    def output(pin, state):
        print(f"Set Pin {pin} to {'HIGH' if state == GPIO.HIGH else 'LOW'}")

    @staticmethod
    def cleanup():
        print("GPIO cleanup complete")
