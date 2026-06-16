#parte 1: setup
import logging, asyncio 
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from influxdb_client import InfluxDBClient

BOT_TOKEN     = '8956350252:AAE_y6PVsD-6D7NZo5rL5rVWo9KiF7hLSgo'
INFLUX_URL    = 'http://localhost:8086'  #influxdb está en nuestro PC
INFLUX_TOKEN  = 'zjh7Xf5323okmz7R4vaQ4G3WMwgF46w8O3aRogu6VM07g9oCQarARgOrWy7FULY6RgMjZmnty0w1IonhMIyVKQ=='  #clave de acceso de influxdb
INFLUX_ORG    = 'unilab'
INFLUX_BUCKET = 'plantas'

logging.basicConfig(level=logging.INFO)

influx = InfluxDBClient(
    url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
qapi = influx.query_api()


def get_datos():
   #q = 'from(bucket:"plantas") |> range(start:-10m) |> last()' #si quisiéramos añadir más métricas esta query se tendría que cambiar como por ejemplo:
    q = '''
    from(bucket: "plantas")
      |> range(start: -10m)
      |> filter(fn: (r) => r._measurement == "sensores_planta")
      |> filter(fn: (r) => r._field == "humedad")
      |> last()
    '''
    #qué te devuelve el último valor tomado de HUMEDAD no de en general
    #en nuestro caso solo almacenamos humedad así que mantenemos la query simple
    #he modificado el bucle así que revisar (si midiésemos más valores también habría que modificar el bucle)
    #esta versión, es más simple (aunque menos escalable) y solo tiene en cuenta la humedad
  
    tablas = qapi.query(q)
    for tabla in tablas:
        for registro in tabla.records:
           
            return {
                "humedad": registro.get_value(),
                "hora": registro.get_time()
            }
    return None
    #así Telegram responde también con la hora a la que ha sido medida la humedad.


#parte 2:comandos

#esta función convierte el dato de humedad en un estado del tamagotchi
def obtener_estado(hum):
    if hum is None:
        return "Desconocido"

    if hum < 30:
        return "Triste"
    elif hum < 60:
        return "Normal"
    else:
        return "Feliz"

#comprueba que exista la hora por si acaso InfluxDB se ralla y convierte el datetime a texto 
def formatear_hora(hora):
    if hora is None:
        return "desconocida"
    #string format time (texto tipo horas: minutos: segundos)
    return hora.strftime("%H:%M:%S")

#cuando el usuario escribe /start (u es el mensaje recibido y ctx es el contexto del robot)
async def cmd_start(u: Update, ctx: ContextTypes.DEFAULT_TYPE):
    txt = (
        "Hola! Soy el monitor de tu planta.\n"
        "/estado — ver estado actual\n"
        "/ayuda — mostrar esta ayuda"
    )
    #espera a la respuesta al chat de Telegram (librería Telegram es asincrónica)
    await u.message.reply_text(txt)
    
#cuando el usuario escribe /ayuda
async def cmd_ayuda(u: Update, ctx: ContextTypes.DEFAULT_TYPE):
    txt = (
        "Este bot permite consultar el estado de la planta en tiempo real.\n\n"
        "Estados:\n"
        "Triste — humedad inferior al 30%\n"
        "Normal — humedad entre 30% y 59%\n"
        "Feliz — humedad igual o superior al 60%\n\n"
        "Comandos:\n"
        "/estado — ver humedad actual y hora de la última medición\n"
        "/ayuda — mostrar esta ayuda"
    )

    await u.message.reply_text(txt)
#cuando el usuario escribe /estado
async def cmd_estado(u: Update, ctx: ContextTypes.DEFAULT_TYPE):
    #llama a la función get_datos() de la parte 1
    datos = get_datos()

    if datos is None:
        await u.message.reply_text("Sin datos recientes. Comprueba que la Pico W esté funcionando.")
        return

    humedad = datos.get("humedad")
    hora = datos.get("hora")

    if humedad is None:
        await u.message.reply_text("No se ha encontrado el dato de humedad en InfluxDB.")
        return

    estado = obtener_estado(humedad)
    hora_txt= formatear_hora(hora)

    await u.message.reply_text(
        f"Estado: {estado}\n"
        f"Humedad suelo: {humedad:.1f}%\n"
        f"Última lectura: {hora_txt}"
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("estado", cmd_estado))
    app.add_handler(CommandHandler("ayuda", cmd_ayuda))

    print("Bot activo...")
    app.run_polling()


if __name__ == "__main__":
    main()

