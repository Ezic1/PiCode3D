
# Pi Control 3D

Este codigo controla un Hardware especial encargado de manejar una impresora 3D a travez de MQTT.

│
├── main.py                  # Punto de entrada. Inicia todo.
├── config/
│   ├── settings.json        # Configuración persistente (como en ESP32)
│   └── config.py            # Carga y guarda configuraciones
│
├── hardware/
│   ├── gpio_pins.py         # Definición de pines
│   ├── relay.py             # Clase Relay
│   ├── fan.py               # Clase Fan
│   ├── buzzer.py            # Clase Buzzer
│   ├── button.py            # Clase Button
│   └── led.py               # Clase LED
│
├── services/
│   ├── mqtt_client.py       # Maneja MQTT (con reconexión automática)
│   ├── octoprint_client.py  # Comunicación con OctoPrint
│   └── system_monitor.py    # Temperaturas, CPU, RAM
│
├── tasks/
│   ├── task_button.py       # Tarea async del botón
│   ├── task_fan.py          # Tarea async ventilador
│   ├── task_buzzer.py       # Tarea async del buzzer
│   ├── task_mqtt.py         # Publicación y suscripción MQTT
│   └── task_led.py          # LED statuss
│
└── utils/
    ├── logger.py            # Sistema de logs
    └── async_helpers.py     # Funciones async reutilizables