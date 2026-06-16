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
write_api = InfluxDBClient(
    url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG
).write_api(write_options=SYNCHRONOUS)
def on_connect(client, ud, flags, rc):
    print(f'Broker conectado (rc={rc})')
    client.subscribe(MQTT_TOPIC)
def on_message(client, ud, msg):
    try:
        data = json.loads(msg.payload)
        p = Point('sensores_planta')
        for campo in ('humedad','temperatura','humedad_aire'):
            if data.get(campo) is not None:
                p.field(campo, float(data[campo]))
        write_api.write(bucket=INFLUX_BUCKET, record=p)
        print('Guardado:', data)
    except Exception as e:
        print('Error:', e)
c = mqtt.Client()
c.on_connect = on_connect
c.on_message = on_message
c.connect(MQTT_BROKER, 1883, 60)
print('Escuchando MQTT...')
c.loop_forever()
