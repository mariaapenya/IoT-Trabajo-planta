from machine import Pin, SPI
import time
import config


class OledDisplay:

    def __init__(self):

        self.spi = SPI(
            0,
            baudrate=10_000_000,
            polarity=0,
            phase=0,
            sck=Pin(config.SPI_SCK),
            mosi=Pin(config.SPI_MOSI)
        )

        self.cs = Pin(config.LCD_CS, Pin.OUT)
        self.dc = Pin(config.LCD_DC, Pin.OUT)
        self.rst = Pin(config.LCD_RST, Pin.OUT)

        self.cs.value(1)
        self.dc.value(1)

        self.init_lcd()

        self.actual = None

    # ----------------------------
    # LOW LEVEL
    # ----------------------------
    def cmd(self, c):
        self.cs.value(0)
        self.dc.value(0)
        self.spi.write(bytearray([c]))
        self.cs.value(1)

    def data(self, d):
        self.cs.value(0)
        self.dc.value(1)
        self.spi.write(bytearray([d]))
        self.cs.value(1)

    # ----------------------------
    # INIT
    # ----------------------------
    def init_lcd(self):

        self.rst.value(0)
        time.sleep(0.1)
        self.rst.value(1)
        time.sleep(0.1)

        self.cmd(0x01)  # SWRESET
        time.sleep(0.15)

        self.cmd(0x11)  # SLPOUT
        time.sleep(0.2)

        self.cmd(0x3A)  # COLMOD
        self.data(0x05) # 16-bit

        self.cmd(0x29)  # DISPON

    # ----------------------------
    # WINDOW
    # ----------------------------
    def set_window(self):

        self.cmd(0x2A)
        self.data(0x00); self.data(0x00)
        self.data(0x00); self.data(0x7F)

        self.cmd(0x2B)
        self.data(0x00); self.data(0x00)
        self.data(0x00); self.data(0x9F)

        self.cmd(0x2C)

    # ----------------------------
    # MOSTRAR IMAGEN RAW
    # ----------------------------
    def show_raw(self, file):

        self.set_window()

        self.cs.value(0)
        self.dc.value(1)

        with open(file, "rb") as f:
            while True:
                buf = f.read(512)
                if not buf:
                    break
                self.spi.write(buf)

        self.cs.value(1)

    # ----------------------------
    # LÓGICA TAMAGOTCHI
    # ----------------------------
    def actualizar(self, humedad):

        if humedad >= config.UMBRAL_BIEN:
            img = config.IMG_FELIZ

        elif humedad >= config.UMBRAL_SECO:
            img = config.IMG_NORMAL

        else:
            img = config.IMG_TRISTE

        if img != self.actual:
            self.actual = img
            self.show_raw(img)
