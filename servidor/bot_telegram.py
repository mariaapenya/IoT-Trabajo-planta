#parte 1: setup
import logging, asyncio
from telegram 
import Update
from telegram.ext 
import Application, CommandHandler, ContextTypes
from influxdb_client 
import InfluxDBClient

BOT_TOKEN     = 'TU_TOKEN_BOTFATHER'
INFLUX_URL    = 'http://localhost:8086'  #influxdb está en nuestro PC
INFLUX_TOKEN  = 'TU_TOKEN_INFLUXDB'  #clave de acceso de influxdb
INFLUX_ORG    = 'unilab'
INFLUX_BUCKET = 'plantas'

logging.basicConfig(level=logging.INFO)

influx = InfluxDBClient(
    url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
qapi = influx.query_api()

def get_datos():
    q = 'from(bucket:"plantas") |> range(start:-10m) |> last()' #si quisiéramos añadir más métricas esta query se tendría que cambiar como por ejemplo:
    #    query = '''
    #from(bucket: "plantas")
      #|> range(start: -10m)
      #|> filter(fn: (r) => r._measurement == "sensores_planta")
      #|> filter(fn: (r) => r._field == "humedad")
      #|> last()
    #'''
    #qué te devuelve el último valor tomado de HUMEDAD no de en general
    #en nuestro caso solo almacenamos humedad así que mantenemos la query simple
    #he modificado el bucle así que revisar (si midiésemos más valores también habría que modificar el bucle)
    #esta versión devuelve un número, es más simple (aunque menos escalable) y solo tiene en cuenta la humedad
    #se podría hacer otra versión que devuelva un diccionario con diferentes parámetros
  
    tablas = query_api.query(q)
    for tabla in tablas:
        for registro in tabla.records:
            return {
                "humedad": registro.get_value(),
                "hora": registro.get_time()
            }
    return None
    #así Telegram responde también con la hora a la que ha sido medida la humedad.


#parte 2:comandos

def obtener_estado(hum):
    if not isinstance(hum, (int, float)):
        return "Desconocido"

    if hum < 30:
        return "Triste"
    elif hum < 60:
        return "Normal"
    else:
        return "Feliz"

async def cmd_start(u: Update, ctx: ContextTypes.DEFAULT_TYPE):
    txt = (
        "Hola! Soy el monitor de tu planta.\n"
        "/estado — ver estado actual\n"
        "/ayuda — mostrar esta ayuda"
    )

    await u.message.reply_text(txt)

async def cmd_ayuda(u: Update, ctx: ContextTypes.DEFAULT_TYPE):
    txt = (
        "Este bot permite consultar el estado de la planta en tiempo real.\n\n"
        "Estados:\n"
        "Triste — humedad inferior al 30%\n"
        "Normal — humedad entre 30% y 59%\n"
        "Feliz — humedad igual o superior al 60%\n\n"
        "Comandos:\n"
        "/estado — ver humedad actual\n"
        "/ayuda — mostrar esta ayuda"
    )

    await u.message.reply_text(txt)

async def cmd_estado(u: Update, ctx: ContextTypes.DEFAULT_TYPE):
    d = get_datos()

    if not d:
        await u.message.reply_text("Sin datos recientes. Comprueba que la Pico W esté funcionando.")
        return

    hum = d.get("humedad")

    if hum is None:
        await u.message.reply_text("No se ha encontrado el dato de humedad en InfluxDB.")
        return

    estado = obtener_estado(hum)

    await u.message.reply_text(
        f"Estado: {estado}\n"
        f"Humedad suelo: {hum:.1f}%"
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

