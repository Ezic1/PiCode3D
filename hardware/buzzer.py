#buzzer.py

import asyncio
from gpiozero import OutputDevice

class Buzzer:
    def __init__(self, pin):
        self._dev = OutputDevice(pin)
        self._continuous_task = None

    def on(self):
        self._dev.on()

    def off(self):
        self._dev.off()

    async def beep(self, duration=0.1):
        self.on()
        await asyncio.sleep(duration)
        self.off()

    async def beep_times(self, n=1, duration=0.1, interval=0.1):
        for _ in range(n):
            await self.beep(duration)
            await asyncio.sleep(interval)

    async def beep_pattern(self, pattern):
        """
        pattern = [(beep_duration, silence_duration), ...]
        """
        for beep_dur, silent_dur in pattern:
            self.on()
            await asyncio.sleep(beep_dur)
            self.off()
            await asyncio.sleep(silent_dur)

    async def alert_success(self):
        await self.beep_times(2, duration=0.07, interval=0.05)

    async def alert_error(self):
        pattern = [
            (0.25, 0.15),
            (0.25, 0.0)
        ]
        await self.beep_pattern(pattern)

    async def _continuous_loop(self):
        while True:
            self.on()
            await asyncio.sleep(0.05)
            self.off()
            await asyncio.sleep(0.05)

    def continuous_beep(self):
        """Start a background continuous beep."""
        if self._continuous_task is None:
            self._continuous_task = asyncio.create_task(self._continuous_loop())

    def stop_continuous(self):
        if self._continuous_task:
            self._continuous_task.cancel()
            self._continuous_task = None
            self.off()
