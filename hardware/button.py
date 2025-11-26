# button.py 

import asyncio
from gpiozero import Button as GpioZeroButton
from time import monotonic

class AsyncButton:
    def __init__(self, pin, hold_threshold=1.0, multi_click_window=0.4):
        """
        hold_threshold: tiempo para considerar "presión larga"
        multi_click_window: tiempo para esperar más clicks consecutivos
        """

        self.btn = GpioZeroButton(pin, pull_up=True, bounce_time=0.01)
        self.hold_threshold = hold_threshold
        self.multi_click_window = multi_click_window

        # estado
        self._press_time = None
        self._click_count = 0

        # tasks
        self._click_task = None

        # callbacks
        self.on_press_callback = None
        self.on_release_callback = None
        self.on_clicks_callback = None

        # enganchar eventos gpiozero
        self.btn.when_pressed = self._pressed
        self.btn.when_released = self._released

    # ----------------------------------------------------------------------
    # REGISTRO DE CALLBACKS
    # ----------------------------------------------------------------------
    def on_press(self, func):
        self.on_press_callback = func

    def on_release(self, func):
        self.on_release_callback = func

    def on_clicks(self, func):
        self.on_clicks_callback = func

    # ----------------------------------------------------------------------
    # EVENTOS INTERNOS
    # ----------------------------------------------------------------------
    def _pressed(self):
        # tiempo en que se presionó
        self._press_time = monotonic()

        if self.on_press_callback:
            asyncio.create_task(self.on_press_callback())

    def _released(self):
        if self._press_time is None:
            return  # debería no pasar nunca

        duration = monotonic() - self._press_time
        self._press_time = None

        if self.on_release_callback:
            asyncio.create_task(self.on_release_callback(duration))

        # CLICK DETECTION -----------------------------------------------
        # si la duración es corta → cuenta como click
        if duration < self.hold_threshold:
            self._click_count += 1

            # reiniciar click_task si existe
            if self._click_task and not self._click_task.done():
                self._click_task.cancel()

            # lanza timer para evaluar clicks múltiples
            self._click_task = asyncio.create_task(
                self._click_timer()
            )
        else:
            # presión larga no cuenta como click simple
            self._click_count = 0

    async def _click_timer(self):
        """
        Espera multi_click_window para ver si hubo más clicks
        """
        try:
            await asyncio.sleep(self.multi_click_window)
        except asyncio.CancelledError:
            return

        count = self._click_count
        self._click_count = 0

        if count > 0 and self.on_clicks_callback:
            await self.on_clicks_callback(count)
