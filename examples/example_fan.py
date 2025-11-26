import asyncio
from hardware.fan import AsyncFan
from hardware.gpio_pins import FAN_PWM_PIN, FAN_FB_PIN

async def fan_stalled():
    print("FAN STALLED — no pulses detected!")

async def main():
    fan = AsyncFan(FAN_PWM_PIN, FAN_FB_PIN)

    fan.on_stall(fan_stalled)
    await fan.start()

    print("Set speed 50%")
    await fan.set_speed(0.5)

    for _ in range(10):
        print("RPM:", fan.get_rpm())
        await asyncio.sleep(1)

    await fan.close()

asyncio.run(main())
