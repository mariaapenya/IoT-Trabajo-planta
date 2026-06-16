import time
import ujson
import network
import machine
from umqtt.simple import MQTTClient
import time
import ujson
from umqtt.simple import MQTTClient

from sensores import leer_humedad_pct
from oled_display import OledDisplay
import config


#inicializar pantalla OLED (interfaz visual del sistema)
oled = OledDisplay()

#crear cliente MQTT con los datos definidos en config.py
cliente = MQTTClient(
    config.MQTT_CLIENT,
    config.MQTT_BROKER,
    config.MQTT_PORT
)


#función para conectar al broker MQTT
def conectar_mqtt():
    try:
        #intenta establecer conexión con el broker
        cliente.connect()
        print("MQTT OK")
        return True
    except Exception as e:
        #si falla la conexión, muestra el error
        print("MQTT error:", e)
        return False


#intentar conexión inicial al broker MQTT al arrancar el programa
conectar_mqtt()


#bucle principal del programa (se ejecuta continuamente)
while True:

    #leer valor de humedad del sensor de suelo
    humedad = leer_humedad_pct()

    #crear payload en formato JSON para enviar por MQTT
    payload = ujson.dumps({
        "humedad": humedad
    })

    #intentar publicar el mensaje en el topic MQTT
    try:
        cliente.publish(config.MQTT_TOPIC, payload)
        print("Publicado:", payload)

    except Exception as e:
        #si falla la publicación, mostrar error y reconectar
        print("MQTT fallo:", e)
        conectar_mqtt()

    #actualizar la pantalla OLED con el valor de humedad
    oled.actualizar(humedad)

    #esperar el intervalo definido antes de la siguiente lectura
    time.sleep(config.INTERVALO_S)
