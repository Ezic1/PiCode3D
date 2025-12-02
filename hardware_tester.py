import time
import sys

# Intentamos importar las clases desde el repo PiCode3D
try:
    from hardware.led import AsyncLed
    from hardware.button import AsyncButton
    from hardware.relay import LatchingRelay
    from hardware.fan import AsyncFan
    from hardware.buzzer import Buzzer
    from hardware.gpio_pins import PINS
except ImportError as e:
    print("ERROR al importar PiCode3D hardware modules:", e)
    print("Asegurate de que el script está ejecutándose desde la carpeta raíz del proyecto PiCode3D.")
    sys.exit(1)


def test_led():
    print("Probando LED...")
    led = AsyncLed(PINS.LED)
    print("Encendiendo LED 2 segundos...")
    led.on()
    time.sleep(2)
    print("Apagando LED...")
    led.off()
    print("LED: prueba OK.")


def test_relay():
    print("Probando Relay...")
    relay = LatchingRelay(PINS.RELAY)
    print("Activando relay 2 segundos...")
    relay.on()
    time.sleep(2)
    print("Desactivando relay...")
    relay.off()
    print("Relay: prueba OK.")


def test_buzzer():
    print("Probando Buzzer...")
    buz = Buzzer()
    print("Activando buzzer 1 segundo...")
    buz.on()
    time.sleep(1)
    print("Apagando buzzer...")
    buz.off()
    print("Buzzer: prueba OK.")


def test_fan():
    print("Probando Fan (ventilador)...")
    fan = AsyncFan(PINS.FAN)
    print("Encendiendo fan 3 segundos...")
    fan.on()
    time.sleep(3)
    print("Apagando fan...")
    fan.off()
    print("Fan: prueba OK.")


def test_button():
    print("Probando Button (espera a una pulsación)...")
    btn = AsyncButton(PINS.BUTTON)
    print("Presioná el botón, Ctrl+C para salir de la prueba.")

    try:
        while True:
            if btn.is_pressed():
                # asumiendo que Button tiene método is_pressed o similar
                print("Botón presionado!")
                # opcional: esperar a que suelte
                while btn.is_pressed():
                    time.sleep(0.1)
                print("Botón liberado — fin de evento.\n")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Saliendo de prueba botón.")


def menu():
    while True:
        print("\n=== TESTER HARDWARE PiCode3D ===")
        print("1) LED")
        print("2) Relay")
        print("3) Buzzer")
        print("4) Fan")
        print("5) Button (entrada)")
        print("q) Salir")

        opt = input("Elegí qué probar: ").strip().lower()
        if opt == "1":
            test_led()
        elif opt == "2":
            test_relay()
        elif opt == "3":
            test_buzzer()
        elif opt == "4":
            test_fan()
        elif opt == "5":
            test_button()
        elif opt == "q":
            break
        else:
            print("Opción inválida.")

    print("Fin de pruebas. Saliendo.")


if __name__ == "__main__":
    menu()
