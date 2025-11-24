# led.py

import asyncio
from gpiozero import OutputDevice

class AsyncLed:
    PWM_FREQUENCY = 1000  # 1 kHz software PWM

    def __init__(self, pin):
        self.dev = OutputDevice(pin, active_high=True)
        self.brightness = 0.0            # Valor 0.0 a 1.0
        self._running = False            # PWM no iniciado aún
        self._pwm_task = None
        self._blink_task = None

    # ---------------------------------------------------------
    #  START / STOP
    # ---------------------------------------------------------
    async def start(self):
        """Inicia el PWM async. Debe llamarse antes de usar."""
        if self._running:
            return

        print("[AsyncLed] Starting PWM loop...")
        self._running = True
        self._pwm_task = asyncio.create_task(self._pwm_loop())

    async def close(self):
        """Apaga el LED y libera tareas."""
        print("[AsyncLed] Closing...")

        await self._stop_blink_task()

        self._running = False

        # permitir que el PWM loop salga
        await asyncio.sleep(0)

        if self._pwm_task:
            try:
                await self._pwm_task
            except asyncio.CancelledError:
                pass

        self.dev.off()
        print("[AsyncLed] Closed")

    # ---------------------------------------------------------
    #  PWM LOOP
    # ---------------------------------------------------------
    async def _pwm_loop(self):
        """Loop interno de 1 kHz usando asyncio."""
        period = 1.0 / self.PWM_FREQUENCY

        while self._running:
            # LED apagado
            if self.brightness <= 0:
                self.dev.off()
                await asyncio.sleep(period)
                continue

            # LED encendido
            if self.brightness >= 1:
                self.dev.on()
                await asyncio.sleep(period)
                continue

            # PWM software
            on_time = period * self.brightness
            off_time = period - on_time

            self.dev.on()
            await asyncio.sleep(on_time)

            self.dev.off()
            await asyncio.sleep(off_time)

        # Salida limpia del loop
        self.dev.off()

    # ---------------------------------------------------------
    #  BASIC FUNCTIONS
    # ---------------------------------------------------------
    async def set_brightness(self, value: float):
        value = max(0.0, min(1.0, value))
        print(f"[AsyncLed] Brightness → {value}")
        self.brightness = value

    async def on(self):
        await self.set_brightness(1.0)

    async def off(self):
        await self.set_brightness(0.0)

    # ---------------------------------------------------------
    #  BLINK FUNCTIONS
    # ---------------------------------------------------------
    async def _stop_blink_task(self):
        """Detiene la tarea de blink si existe."""
        if self._blink_task and not self._blink_task.done():
            self._blink_task.cancel()
            try:
                await self._blink_task
            except asyncio.CancelledError:
                pass
        self._blink_task = None

    async def blink(self, interval_on=0.3, interval_off=0.3):
        """Blink infinito."""
        print("[AsyncLed] Blink ON (infinite)")

        await self._stop_blink_task()

        async def _loop():
            while True:
                await self.on()
                await asyncio.sleep(interval_on)
                await self.off()
                await asyncio.sleep(interval_off)

        self._blink_task = asyncio.create_task(_loop())

    async def blink_times(self, times, interval_on=0.3, interval_off=0.3):
        """Blink N veces (tarea bloqueante)."""
        print(f"[AsyncLed] Blink x{times}")

        await self._stop_blink_task()

        async def _loop():
            for _ in range(times):
                await self.on()
                await asyncio.sleep(interval_on)
                await self.off()
                await asyncio.sleep(interval_off)

        self._blink_task = asyncio.create_task(_loop())
        await self._blink_task      # Espera a que termine
        self._blink_task = None
