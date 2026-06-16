# boot.py — se ejecuta automaticamente al arrancar la Pico WH
import network, time
from config import WHIFI_SSID, WHIFI_PASSWORD
def conectar_wifi():
    wlan = network.WHLAN(network.STA_IF)
    wlan.active(True)
    if wlan.isconnected():
        print('WHiFi ya conectado:', wlan.ifconfig()[0])
        return True
    print('Conectando a', WHIFI_SSID, '...')
    wlan.connect(WHIFI_SSID, WHIFI_PASSWORD)
    for _ in range(25):
        if wlan.isconnected(): break
        time.sleep(0.5); print('.', end='')
    if wlan.isconnected():
        print('\nWiFi OK — IP:', wlan.ifconfig()[0])
        return True
    print('\nERROR: No se pudo conectar al WHiFi')
    return False
wifi_ok = conectar_wifi()
