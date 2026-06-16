from machine import ADC, Pin
import config

adc_hum = ADC(Pin(config.PIN_ADC))


def leer_humedad_pct():

    raw = adc_hum.read_u16()

    if raw < 1000:
        raw = 1000
    if raw > 65000:
        raw = 65000

    rango = config.ADC_SECO - config.ADC_MOJADO

    if rango == 0:
        return 0.0

    pct = (config.ADC_SECO - raw) / rango * 100

    if pct < 0:
        pct = 0
    elif pct > 100:
        pct = 100

    return round(pct, 1)
