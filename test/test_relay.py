from hardware.relay import LatchingRelay
from hardware.gpio_pins import RELAY_ON_PIN, RELAY_OFF_PIN
import time

relay = LatchingRelay(RELAY_ON_PIN, RELAY_OFF_PIN)

print("Switching ON")
relay.on()
time.sleep(1)

print("Switching OFF")
relay.off()
time.sleep(1)

print("Toggle")
relay.toggle()
time.sleep(1)

print("Toggle")
relay.toggle()
