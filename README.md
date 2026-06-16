# IoT-Trabajo-planta
Proyecto IoT Monitor de Plantas

Proyecto desarrollado para la asignatura Internet de las Cosas (IDC) de la Universitat Politècnica de València (UPV).

## Autores:
- Maria Peña Astolfi
- Ana Maria Becerra López

## Descripción
Este proyecto implementa un sistema IoT para monitorizar el estado de una planta mediante una Raspberry Pi Pico W, un sensor de humedad del suelo capacitivo y una pantalla TFT ST7735S a color.

La Raspberry Pi Pico W mide periódicamente la humedad del suelo y publica los datos mediante MQTT. Los datos se almacenan en InfluxDB, se visualizan mediante Grafana y pueden consultarse remotamente mediante un bot de Telegram.

Además, el estado de la planta se representa mediante un personaje tipo Tamagotchi mostrado en la pantalla.

## Características:
- Medición de humedad del suelo en tiempo real.
- Conexión WiFi mediante Raspberry Pi Pico W.
- Comunicación mediante protocolo MQTT.
- Almacenamiento histórico de datos en InfluxDB.
- Visualización gráfica mediante Grafana.
- Consulta remota mediante Telegram.
- Interfaz visual basada en un Tamagotchi a color.

## Hardware utilizado:
- Raspberry Pi Pico W
- Pantalla TFT ST7735S 1.8" (128x160)
- Capacitive Soil Moisture Sensor V1.2
- Protoboard
- Cables Dupont

## Tecnologías utilizadas

### Lenguajes de programación

* **Python 3** para los scripts del servidor y el bot de Telegram.
* **MicroPython** para el desarrollo del firmware de la Raspberry Pi Pico W.

### Protocolos de comunicación

* **WiFi** para la conexión de la Raspberry Pi Pico W a la red.
* **MQTT** para el envío de las medidas de humedad al servidor.

### Bases de datos y almacenamiento

* **InfluxDB 2.x** para el almacenamiento de las medidas de humedad obtenidas por el sensor.

### Visualización de datos

* **Grafana** para la representación gráfica y monitorización de las medidas almacenadas en InfluxDB.

### Servicios y herramientas

* **Mosquitto MQTT Broker** para la gestión de la comunicación MQTT.
* **Telegram Bot API** para la consulta remota del estado de la planta.
* **Git y GitHub** para el control de versiones y la gestión colaborativa del proyecto.


## Arquitectura del sistema

```text
Capacitive Soil Moisture Sensor
                │
                ▼
      Raspberry Pi Pico W
                │
                ▼
              MQTT
                │
                ▼
      mqtt_to_influx.py
                │
                ▼
            InfluxDB
            │      │
            │      └────────────► Bot Telegram
            │
            └───────────────────► Grafana
```

## Estructura del repositorio

```text
IoT-Trabajo-planta/
│
├── pico_w/
│   ├── boot.py
│   ├── config.py
│   ├── main.py
│   ├── sensores.py
│   ├── oled_display.py
│   ├── feliz.raw
│   ├── normal.raw
│   ├── triste.raw
│
├── servidor/
│   ├── mqtt_to_influx.py
│   ├── bot_telegram.py
│   └── requirements.txt
│
├── grafana/
│   └── dashboard.json
│
├── imagenes/
│   └── convertir_png_rgb565.py
│   ├── feliz.raw
│   ├── normal.raw
│   ├── triste.raw
│   ├── feliz.png
│   ├── normal.png
│   ├── triste.png
│
├── docs/
│   ├── memoria.pdf
│   ├── guia_usuario.pdf
│   ├── guia_programador.pdf
│   └── fotos/
│
├── README.md
└── .gitignore
```

## Instalación
### 1. Instalar dependencias Python
pip install -r pc_servidor/requirements.txt

### 2. Instalar servicios necesarios
- Mosquitto MQTT Broker
- InfluxDB 2.x
- Grafana

### Configurar la Raspberry Pi Pico W
Configurar 
- WIFI_SSID
- WIFI_PASSWORD
- MQTT_BROKER
- ADC_SECO
- ADC_MOJADO

## Ejecución
### Iniciar el puente MQTT -> InfluxDB
python pc_servidor/mqtt_to_influx.py

###Iniciar el bot de Telegram
python pc_servidor/bot_telegram.py

### Ejecutar la Pico W
Subir los archivos de la carpeta pico_w mediante Thonny y ejecutar:
main.py

### Estados de la planta
## Estados de la planta

| Humedad del suelo | Estado    | Descripción                                                            |
| ----------------- | --------- | ---------------------------------------------------------------------- |
| < 30 %            | Triste | La planta necesita agua. Se recomienda regarla lo antes posible.       |
| 30 % – 59 %       | Normal | La planta se encuentra en condiciones aceptables.                      |
| ≥ 60 %            | Feliz  | La planta dispone de suficiente humedad y se encuentra en buen estado. |

### Dashboard Grafana
Importar el archivo:
grafana/dashboard.json
desde:
Dashboard -> Import

### Bot de Telegram
Comandos disponibles:

/start
/estado
/ayuda





