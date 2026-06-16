from PIL import Image
import struct
import os

ANCHO = 128
ALTO = 160

IMAGENES = [
    ("feliz.png", "feliz.raw"),
    ("normal.png", "normal.raw"),
    ("triste.png", "triste.raw")
]

def convertir_png(entrada, salida):

    img = Image.open(entrada).convert("RGB")

    if img.size != (ANCHO, ALTO):
        img = img.resize((ANCHO, ALTO))

    with open(salida, "wb") as f:

        for y in range(ALTO):
            for x in range(ANCHO):

                r, g, b = img.getpixel((x, y))

                rgb565 = (
                    ((r & 0xF8) << 8)
                    | ((g & 0xFC) << 3)
                    | (b >> 3)
                )

                f.write(struct.pack(">H", rgb565))

    print(
        salida,
        os.path.getsize(salida),
        "bytes"
    )

for entrada, salida in IMAGENES:

    if os.path.exists(entrada):
        convertir_png(entrada, salida)
    else:
        print("No existe:", entrada)

print("Conversión terminada")
