import asyncio
from hardware.led import AsyncLed
from hardware.gpio_pins import LED_PIN

async def main():
    led = AsyncLed(LED_PIN)

    print("LED brillo 50%")
    await led.set_brightness(0.5)
    await asyncio.sleep(2)

    print("Blink continuo")
    await led.blink(0.2, 0.2)
    await asyncio.sleep(3)

    print("Blink x5")
    await led.blink_times(5, 0.1, 0.1)

    print("Off")
    await led.off()

    await led.close()

asyncio.run(main())
