import asyncio
from hardware.button import AsyncButton
from hardware.gpio_pins import BUTTON_PIN

async def press_event():
    print("Botón PRESIONADO")

async def release_event(duration):
    print(f"Botón LIBERADO — duró {duration:.2f} segundos")

async def clicks_event(count):
    print(f"Botón presionado {count} veces seguidas")

async def main():
    btn = AsyncButton(BUTTON_PIN)

    btn.on_press(press_event)
    btn.on_release(release_event)
    btn.on_clicks(clicks_event)

    print("Esperando eventos...")
    while True:
        await asyncio.sleep(1)

asyncio.run(main())
