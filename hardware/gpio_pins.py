# gpio_pins.py

"""
Archivo central donde se definen todos los pines GPIO usados por el hardware.

"""

# ==========================
# Pines de salida
# ==========================
RELAY_ON_PIN = 17     # Encender energía impresora
RELAY_OFF_PIN = 27    # Apagar energía impresora
BUZZER_PIN = 22       # Buzzer activo
FAN_PIN = 12          # Ventilador para Pi PWM PIN
STATUS_LED_PIN = 23   # LED indicador opcional PWM Simulado

# ==========================
# Pines de entrada
# ==========================
BUTTON_PIN = 21       # Botón físico de power/control
RELAY_STATUS_PIN = 26 # Estado de la relé   

# ==========================
# Pines especiales
# ==========================
I2C_SDA_PIN = 2
I2C_SCL_PIN = 3

UART_TX_PIN = 14
UART_RX_PIN = 15