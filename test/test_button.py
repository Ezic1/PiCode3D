import RPi.GPIO as GPIO
import time

BUTTON_PIN = 21    # Pin BCM
DEBOUNCE_TIME = 0.02  # 20 ms (suave devido a un capacitor de 100nF en hardware)

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setwarnings(False)

# ============================================================
# FUNCIÓN 1: Capturar tiempo de presión
# ============================================================
def medir_tiempo_presionado():
    print("Esperando que presiones el botón...")

    while True:
        # Espera a que el botón se PRESIONE (nivel bajo)
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            inicio = time.time()

            # Espera a que el botón se SUELTE
            while GPIO.input(BUTTON_PIN) == GPIO.LOW:
                time.sleep(DEBOUNCE_TIME)

            fin = time.time()
            duracion = fin - inicio

            print(f"Botón presionado durante {duracion:.2f} segundos")
            return duracion


# ============================================================
# FUNCIÓN 2: Contar cantidad de pulsos
# ============================================================
def contar_pulsos(tiempo_ventana=3):
    """
    Cuenta cuántas veces se presionó el botón dentro de una ventana de tiempo.
    Por defecto: 3 segundos.
    """

    print(f"Contando pulsos por {tiempo_ventana} segundos...")
    contador = 0
    tiempo_inicio = time.time()

    boton_anterior = GPIO.input(BUTTON_PIN)

    while time.time() - tiempo_inicio < tiempo_ventana:
        estado = GPIO.input(BUTTON_PIN)

        # Detectar flanco descendente (transición de "no presionado" → "presionado")
        if boton_anterior == GPIO.HIGH and estado == GPIO.LOW:
            contador += 1
            print("→ Botón presionado!")

        boton_anterior = estado
        time.sleep(DEBOUNCE_TIME)

    print(f"Botón presionado {contador} veces")
    return contador


# ============================================================
# MODO DEMO: probar ambas funciones
# ============================================================
def main():
    try:
        setup()

        while True:
            print("\n=== MENU ===")
            print("1) Medir tiempo presionado")
            print("2) Contar pulsos (3 segundos)")
            print("q) Salir")

            opcion = input("Selecciona: ")

            if opcion == "1":
                medir_tiempo_presionado()

            elif opcion == "2":
                contar_pulsos()

            elif opcion == "q":
                break

            else:
                print("Opción inválida.")

    except KeyboardInterrupt:
        print("\nSaliendo...")

    finally:
        GPIO.cleanup()
        print("GPIO liberado.")


if __name__ == "__main__":
    main()
