from PIL import Image

def rgb565(r, g, b):
    return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

img = Image.open("../assets/feliz.jpeg")
img = img.resize((64, 64))
img = img.convert("RGB")

datos = []

for r, g, b in img.getdata():
    color = rgb565(r, g, b)
    datos.append((color >> 8) & 0xFF)
    datos.append(color & 0xFF)

with open("sprite_feliz.bin", "wb") as f:
    f.write(bytearray(datos))
