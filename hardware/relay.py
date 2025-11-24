# relay.py

from gpiozero import OutputDevice
import time
from .base_device import BaseDevice
from hardware.gpio_pins import RELAY_ON_PIN, RELAY_OFF_PIN

class LatchingRelay(BaseDevice):
    def __init__(self, pin_on, pin_off, pulse_time_ms=50):
        super().__init__("LatchingRelay")
        self.pin_on = OutputDevice(pin_on, active_high=True)
        self.pin_off = OutputDevice(pin_off, active_high=True)
        self.pulse_time = pulse_time_ms / 1000.0  # convertir ms a s
        self._state = None  # True = ON, False = OFF

    def _pulse(self, device):
        self.log(f"Pulsing {device} for {self.pulse_time}s")
        device.on()
        time.sleep(self.pulse_time)
        device.off()

    def on(self):
        if self._state is True:
            self.log("Already ON — no action")
            return
        self.log("Switching to ON")
        self._pulse(self.pin_on)
        self._state = True

    def off(self):
        if self._state is False:
            self.log("Already OFF — no action")
            return
        self.log("Switching to OFF")
        self._pulse(self.pin_off)
        self._state = False

    def toggle(self):
        if self._state:
            self.off()
        else:
            self.on()

    def state(self):
        return self._state
