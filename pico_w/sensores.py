# sensores.py: leer los sensores físicos y devolver los valores ya preparados para que main los use
from machine import ADC, Pin
import dht
import config

adc_hum = ADC(Pin(config.PIN_HUMEDAD))
dht22   = dht.DHT22(Pin(config.PIN_DHT22))

def leer_humedad_pct():
  #función que lee la humedad del suelo y la convierte a porcentaje 
    raw = adc_hum.read_u16()
    pct = (config.ADC_SECO - raw) / (config.ADC_SECO - config.ADC_MOJADO) * 100
    return max(0.0, min(100.0, round(pct, 1)))
  
def leer_dht22():
    try:
        dht22.measure()
        return dht22.temperature(), dht22.humidity()
    except Exception as e:
        print('DHT22 error:', e)
        return None, None
