# sensores.py: leer los sensores físicos y devolver los valores ya preparados para que main los use
from machine import ADC, Pin
import config

adc_hum = ADC(Pin(config.PIN_HUMEDAD))

def leer_humedad_pct():
  #función que lee la humedad del suelo y la convierte a porcentaje 
    raw = adc_hum.read_u16()
    pct = (config.ADC_SECO - raw) / (config.ADC_SECO - config.ADC_MOJADO) * 100
    return max(0.0, min(100.0, round(pct, 1)))
  
