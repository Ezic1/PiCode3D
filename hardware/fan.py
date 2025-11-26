# fan.py

import asyncio
from gpiozero import PWMOutputDevice, Button
from time import monotonic

class AsyncFan:
    def __init__(self, pwm_pin, fb_pin, pulses_per_rev=2, rpm_interval=1.0):
        """
        pwm_pin: pin GPIO con PWM hardware
        fb_pin: pin GPIO para el feedback (pulsos)
        pulses_per_rev: la mayoría de los fans son 2 pulsos por vuelta
        rpm_interval: cada cuántos segundos se calcula el RPM
        """

        self.pwm = PWMOutputDevice(pwm_pin, active_high=True, frequency=25000)  # 25kHz típico para fans
        self.fb = Button(fb_pin, pull_up=True, bounce_time=None)

        self.pulses_per_rev = pulses_per_rev
        self.rpm_interval = rpm_interval

        self._pulse_count = 0
        self._current_rpm = 0
        self._running = False
        self._rpm_task = None

        # detectar flancos de subida
        self.fb.when_pressed = self._pulse_detected

        # callbacks de seguridad opcional
        self.on_stall_callback = None
        self._stall_timeout = 3  # segundos sin pulsos para detectar fan trabado
        self._last_pulse_time = monotonic()

    # ----------------------------------------------------------------------
    # CALLBACKS
    # ----------------------------------------------------------------------
    def on_stall(self, func):
        """Callback si el fan se queda sin pulsos (posible trabado)."""
        self.on_stall_callback = func

    # ----------------------------------------------------------------------
    # EVENTOS INTERNOS
    # ----------------------------------------------------------------------
    def _pulse_detected(self):
        self._pulse_count += 1
        self._last_pulse_time = monotonic()

    # ----------------------------------------------------------------------
    # RPM LOOP
    # ----------------------------------------------------------------------
    async def _rpm_loop(self):
        while self._running:
            # guardar y resetear
            pulses = self._pulse_count
            self._pulse_count = 0

            # calcular RPM
            if pulses > 0:
                self._current_rpm = (pulses / self.pulses_per_rev) * 60
            else:
                self._current_rpm = 0

            # stall detection
            if monotonic() - self._last_pulse_time > self._stall_timeout:
                if self.on_stall_callback:
                    await self.on_stall_callback()

            await asyncio.sleep(self.rpm_interval)

    # ----------------------------------------------------------------------
    # CONTROL
    # ----------------------------------------------------------------------
    async def start(self):
        if self._running:
            return
        self._running = True
        self._rpm_task = asyncio.create_task(self._rpm_loop())

    async def close(self):
        self._running = False
        if self._rpm_task:
            try:
                await self._rpm_task
            except asyncio.CancelledError:
                pass
        self.pwm.value = 0

    # ----------------------------------------------------------------------
    # USER API
    # ----------------------------------------------------------------------
    async def set_speed(self, duty: float):
        """Define la velocidad (0.0 a 1.0)."""
        duty = max(0.0, min(1.0, duty))
        self.pwm.value = duty

    def get_duty(self):
        return self.pwm.value

    def get_rpm(self):
        return self._current_rpm
