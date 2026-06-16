import time
import ujson
from umqtt.simple import MQTTClient

from sensores import leer_humedad_pct
from oled_display import OledDisplay
import config


oled = OledDisplay()

cliente = MQTTClient(
    config.MQTT_CLIENT,
    config.MQTT_BROKER,
    config.MQTT_PORT
)


def conectar_mqtt():
    try:
        cliente.connect()
        print("MQTT OK")
        return True
    except Exception as e:
        print("MQTT error:", e)
        return False


conectar_mqtt()


while True:

    humedad = leer_humedad_pct()

    payload = ujson.dumps({
        "humedad": humedad
    })

    try:
        cliente.publish(config.MQTT_TOPIC, payload)
        print("Publicado:", payload)

    except Exception as e:
        print("MQTT fallo:", e)
        conectar_mqtt()

    oled.actualizar(humedad)

    time.sleep(config.INTERVALO_S)
