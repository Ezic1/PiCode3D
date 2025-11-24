# led.py

import asyncio
from gpiozero import OutputDevice

class AsyncLed:
    PWM_FREQUENCY = 1000  # 1 kHz
    
    def __init__(self, pin):
        self.dev = OutputDevice(pin, active_high=True)
        self.brightness = 0.0   # 0.0 to 1.0
        self._running = True
        self._pwm_task = asyncio.create_task(self._pwm_loop())
        self._blink_task = None

    async def _pwm_loop(self):
        """PWM software async (1 kHz)."""
        period = 1.0 / self.PWM_FREQUENCY  # ~0.001s

        while self._running:
            if self.brightness <= 0:
                self.dev.off()
                await asyncio.sleep(period)
                continue

            if self.brightness >= 1:
                self.dev.on()
                await asyncio.sleep(period)
                continue

            # Duty cycle
            on_time = period * self.brightness
            off_time = period - on_time

            self.dev.on()
            await asyncio.sleep(on_time)
            self.dev.off()
            await asyncio.sleep(off_time)

    # -----------------------------
    # Basic functions
    # -----------------------------

    async def on(self):
        self.brightness = 1.0

    async def off(self):
        self.brightness = 0.0

    async def set_brightness(self, value: float):
        """value: 0.0 to 1.0"""
        value = max(0.0, min(1.0, value))
        self.brightness = value

    # -----------------------------
    # Blink functions
    # -----------------------------

    async def _stop_blink_task(self):
        if self._blink_task and not self._blink_task.done():
            self._blink_task.cancel()
            try:
                await self._blink_task
            except asyncio.CancelledError:
                pass
        self._blink_task = None

    async def blink(self, interval_on=0.3, interval_off=0.3):
        """Blink indefinitely."""
        await self._stop_blink_task()

        async def _blink_loop():
            while True:
                await self.on()
                await asyncio.sleep(interval_on)
                await self.off()
                await asyncio.sleep(interval_off)

        self._blink_task = asyncio.create_task(_blink_loop())

    async def blink_times(self, times, interval_on=0.3, interval_off=0.3):
        """Blink a fixed number of times."""
        await self._stop_blink_task()

        async def _blink_x():
            for _ in range(times):
                await self.on()
                await asyncio.sleep(interval_on)
                await self.off()
                await asyncio.sleep(interval_off)

        self._blink_task = asyncio.create_task(_blink_x())
        await self._blink_task
        self._blink_task = None

    # -----------------------------
    # Shutdown
    # -----------------------------

    async def close(self):
        """Stop PWM cleanly."""
        await self._stop_blink_task()
        self._running = False
        await asyncio.sleep(0)  # yield to stop PWM loop
        self.dev.off()
