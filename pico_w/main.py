from sensores import leer_humedad
from tamagotchi import obtener_estado
from pantalla import mostrar_estado

while True:

    humedad = leer_humedad()

    estado = obtener_estado(humedad)

    mostrar_estado(estado)
