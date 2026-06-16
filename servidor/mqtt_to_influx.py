# mqtt_to_influx.py
import json
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

MQTT_BROKER   = 'localhost'
MQTT_TOPIC    = 'planta/sensores'
INFLUX_URL    = 'http://localhost:8086'
INFLUX_TOKEN  = 'TU_TOKEN_INFLUXDB'
INFLUX_ORG    = 'unilab'
INFLUX_BUCKET = 'plantas'

#crea el objeto que permite escribir datos en InfluxDB
write_api = InfluxDBClient(
    url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG
).write_api(write_options=SYNCHRONOUS)

#cuando se conecta a Mosquitto rc es el código de resultado, si es 0 is okay
def on_connect(client, ud, flags, rc):
    print(f'Broker conectado (rc={rc})')
    client.subscribe(MQTT_TOPIC)
#se reciben todos los mensajes publicados en planta/sensores

#cada vez que llega un mensaje
def on_message(client, ud, msg):
    try:
        data = json.loads(msg.payload)
        #crea un punto de InfluxDB llamado sensores_planta (que luego se usa en Grafana y en las queries)
        p = Point('sensores_planta')
        #solo guardamos la humedad del suelo
        if data.get('humedad') is not None:
            p.field('humedad', float(data['humedad']))
        else:
            print('Mensaje recibido sin campo humedad:', data)
            return
        #guarda el punto en el bucket plantas
        write_api.write(bucket=INFLUX_BUCKET, record=p)
        #y muestra en terminal que el dato se ha guardado correctamente
        print('Guardado:', data)
        
    #control de errores
    except Exception as e:
        print('Error:', e)

#crear cliente mqtt
c = mqtt.Client()
c.on_connect = on_connect
c.on_message = on_message
#conecta mosquitto en localhost y cada 60 segundos comprueba si se mantiene la conexión (keep alive)
c.connect(MQTT_BROKER, 1883, 60)
print('Escuchando MQTT...')
c.loop_forever()
