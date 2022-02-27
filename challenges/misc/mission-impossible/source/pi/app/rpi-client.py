#!/usr/bin/python3

VIRTUAL_PI = False

try:
    import RPi.GPIO as GPIO
except ImportError:
    print("WARNING - Enabling virtual pi mode", flush=True)
    VIRTUAL_PI = True

import time
import requests
import signal
import sys

# How often to poll the server.
POLL_SLEEP = 1000   # ms.

# How long to sleep on connection error.
ERROR_TIMEOUT = 5000    # ms.

HOST = "http://137.184.230.206:5000" 
ENDPOINT = "/7ETfKgw4NYND9JMStKNVuSpjLDCB6y/laser-state"

SOUND_SERVER_HOST = "http://192.168.1.32:5000"
SOUND_SERVER_ENDPOINT= "/sound"

class LaserHandler:
    def __init__(self):
        self._error = True
        self._prev_state = None

        self.init_gpio()

    def init_gpio(self):
        """
        Initialize the GPIO pins.
        """
        if not VIRTUAL_PI:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(17, GPIO.OUT, initial=GPIO.HIGH)
            GPIO.setup(18, GPIO.OUT, initial=GPIO.HIGH)
            GPIO.setup(22, GPIO.OUT, initial=GPIO.HIGH)
            GPIO.setup(23, GPIO.OUT, initial=GPIO.HIGH)

    def run(self):
        """
        Start the run-loop.
        """
        while True:
            # Connect to status server.
            try:
                r = requests.get(f"{HOST}{ENDPOINT}")
                json_data = r.json()
            except Exception as e:
                self.handle_error(f"Unable to connect to {HOST}{ENDPOINT}: {e}")
                continue

            # Parse the json data.
            try:
                normalized = [x["State"] for x in json_data]

                self.log_pins(normalized)
                self.update_pins(normalized)
                self.check_win(normalized)

            except ValueError as e:
                self.handle_error(f"Invalid json data: {e}")
                continue

            if self._error:
                self._error = False
                self.log_success("Connection to host recovered")

            msleep(POLL_SLEEP)

    def check_win(self, normalized_data):
        if 1 in normalized_data:
            return

        msleep(1500)

        self.log_success("Playing win animation")
        
        self.send_sound("win")

        sleep_amount=300

        if not VIRTUAL_PI:
            # Switch animation
            for x in range(5):
                GPIO.output(17, GPIO.HIGH)
                GPIO.output(18, GPIO.HIGH)
                GPIO.output(22, GPIO.LOW)
                GPIO.output(23, GPIO.LOW)
                msleep(sleep_amount)
                GPIO.output(17, GPIO.LOW)
                GPIO.output(18, GPIO.LOW)
                GPIO.output(22, GPIO.HIGH)
                GPIO.output(23, GPIO.HIGH)
                msleep(sleep_amount)
                GPIO.output(17, GPIO.HIGH)
                GPIO.output(18, GPIO.LOW)
                GPIO.output(22, GPIO.HIGH)
                GPIO.output(23, GPIO.LOW)
                msleep(sleep_amount)
                GPIO.output(17, GPIO.LOW)
                GPIO.output(18, GPIO.HIGH)
                GPIO.output(22, GPIO.LOW)
                GPIO.output(23, GPIO.HIGH)
                msleep(sleep_amount)

        self.reset_pins()
        msleep(3000)

    def send_sound(self, state):
        """
        Send an sound request to the sound server.
        """
        try:
            requests.post(f"{SOUND_SERVER_HOST}{SOUND_SERVER_ENDPOINT}", json={"state": state}, timeout=1)
        except (requests.exceptions.ReadTimeout, requests.exceptions.ReadTimeout): 
            pass
        except requests.exceptions.RequestException as e:
            self.log_error(f"Unable to connect to sound server: {e}")

    def update_pins(self, normalized_data):
        """
        Update the power level of the GPIO pins based on the json data.
        """
        if 0 in normalized_data:
            self.send_sound("powerdown")

        if not VIRTUAL_PI:
            try:
                if normalized_data[0]:
                    GPIO.output(17, GPIO.HIGH)
                else:
                    GPIO.output(17, GPIO.LOW)

                if normalized_data[1]:
                    GPIO.output(18, GPIO.HIGH)
                else:
                    GPIO.output(18, GPIO.LOW)

                if normalized_data[2]:
                    GPIO.output(22, GPIO.HIGH)
                else:
                    GPIO.output(22, GPIO.LOW)

                if normalized_data[3]:
                    GPIO.output(23, GPIO.HIGH)
                else:
                    GPIO.output(23, GPIO.LOW)

            except KeyError as e:
                self.handle_error(f"Invalid json data: {e}")
                return

        msleep(3000)

    def reset_pins(self):
        """
        Reset the pins to their high values.
        """
        if not VIRTUAL_PI:
            GPIO.output(17, GPIO.HIGH)
            GPIO.output(18, GPIO.HIGH)
            GPIO.output(22, GPIO.HIGH)
            GPIO.output(23, GPIO.HIGH)

    def handle_error(self, data):       
        """
        Handle an error fetching the laser state.
        """ 
        self._error = True
        self.log_error(data)

        self.reset_pins()
        msleep(ERROR_TIMEOUT)

    def log_pins(self, normalized_data):
        """
        Log the output of the pins if they have changed.
        """
        if normalized_data == self._prev_state:
            return

        self._prev_state = normalized_data

        if not 0 in normalized_data:
            self.log_success("Laser state reset")
            return

        to_log = []
        for i, x in enumerate(normalized_data):
            if not x:
                to_log.append(f"laser{i}")

        self.log_success(f"Lasers shut down: {to_log}")

    def log_success(self, data):
        """
        Log successful message.
        """
        print(f"\033[92m[{time.strftime('%Y-%m-%d %H:%M:%S')}]\033[0m {data}", flush=True)

    def log_error(self, data):
        """
        Log error message.
        """
        print(f"\033[91m[{time.strftime('%Y-%m-%d %H:%M:%S')}]\033[0m {data}", file=sys.stderr, flush=True)


def signal_handler(sig, frame):
    """
    Custom SIGINT handler.
    Cleans up the GPIO pin state.
    """

    print("Stopping...", flush=True)

    if not VIRTUAL_PI:
        GPIO.cleanup()

    print("Stopped.", flush=True)
    sys.exit(0)

def msleep(ms):
    time.sleep(ms / 1000)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print(f"\n{time.strftime('%Y-%m-%d %H:%M:%S')}\n", flush=True)
    print(f"Endpoint: {HOST}{ENDPOINT}", flush=True)
    print(f"Polling: {POLL_SLEEP} ms.", flush=True)
    print(f"Error timeout: {ERROR_TIMEOUT} ms.\n", flush=True)

    laser_handler = LaserHandler()
    laser_handler.run()

if __name__ == "__main__":
    main()
