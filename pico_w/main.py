import time
import ujson
from umqtt.simple 
import MQTTClient
from sensores 
import leer_humedad_pct
from oled_display 
import OledDisplay
import config

#iniciar la pantalla (cuidado porque es otra)
oled   = OledDisplay()

#iniciar cliente MQTT
cliente = MQTTClient(config.MQTT_CLIENT, config.MQTT_BROKER, config.MQTT_PORT)
def conectar_mqtt():
    try:
        cliente.connect()
        print('MQTT OK ->', config.MQTT_BROKER)
        return True
    except Exception as e:
        print('MQTT error:', e); 
        return False
conectar_mqtt()

while True:
    #lee la humedad del suelo
    humedad = leer_humedad_pct()
    #mensaje JSON no es necesario en verdad pero simplifica mucho y para futuras ampliaciones
    payload = ujson.dumps({
        "humedad": humedad
    })

    #publicar datos por MQTT
    try:
        cliente.publish(config.MQTT_TOPIC, payload)
        print("Publicado:", payload)

    except Exception as e:
        print("Error publicando MQTT:", e)
        conectar_mqtt()

    #actualizar Tamagotchi en pantalla con la función en oled_display.py
    oled.actualizar(humedad)

    # Esperar hasta la siguiente lectura
    time.sleep(config.INTERVALO_S)
