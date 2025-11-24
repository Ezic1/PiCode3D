import asyncio
from hardware.led import AsyncLed
from hardware.gpio_pins import STATUS_LED_PIN

async def main():
    led = AsyncLed(STATUS_LED_PIN)
    await led.start()

    print("Brillo 30%")
    await led.set_brightness(0.3)
    await asyncio.sleep(2)

    print("Blink infinito")
    await led.blink(0.1, 0.1)
    await asyncio.sleep(3)

    print("Blink x5")
    await led.blink_times(5, 0.05, 0.05)

    print("OFF")
    await led.off()

    await led.close()

asyncio.run(main())
