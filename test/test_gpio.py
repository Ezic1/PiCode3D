import RPi.GPIO as GPIO
import time

# ==========================
# CONFIGURACIÓN
# ==========================
LED_PIN = 23        # 
BUTTON_PIN = 21     # 
BLINK_TIME = 0.5    # segundos

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Pin LED como salida
    GPIO.setup(LED_PIN, GPIO.OUT)

    # Pin botón como entrada con PULL-UP interno
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def test_output():
    print("\n--- Prueba de salida (LED) ---")
    print("Parpadeando 5 veces…")

    for i in range(5):
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(BLINK_TIME)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(BLINK_TIME)

    print("Listo!\n")

def test_input():
    print("--- Prueba de entrada (Botón) ---")
    print("Mantén o suelta el botón para ver el estado. Ctrl+C para salir.\n")

    try:
        while True:
            if GPIO.input(BUTTON_PIN) == GPIO.LOW:
                print("Botón PRESIONADO")
            else:
                print("Botón SUELTO")
            time.sleep(0.2)

    except KeyboardInterrupt:
        print("\nFinalizando prueba…")

def cleanup():
    GPIO.cleanup()
    print("GPIO limpio.")

if __name__ == "__main__":
    setup()
    test_output()
    test_input()
    cleanup()
