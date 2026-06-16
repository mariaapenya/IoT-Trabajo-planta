import network
import time
import config


def conectar_wifi():

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if wlan.isconnected():
        print("WiFi ya conectado:", wlan.ifconfig()[0])
        return True

    print("Conectando a WiFi:", config.WIFI_SSID)
    wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)

    for _ in range(25):
        if wlan.isconnected():
            break
        time.sleep(0.5)
        print(".", end="")

    if wlan.isconnected():
        print("\nWiFi OK:", wlan.ifconfig()[0])
        return True

    print("\nERROR WiFi")
    return False


wifi_ok = conectar_wifi()
