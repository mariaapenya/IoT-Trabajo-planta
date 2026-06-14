def obtener_estado(humedad):

    if humedad < 10:
        return "muerta"

    elif humedad < 30:
        return "triste"

    elif humedad < 70:
        return "normal"

    else:
        return "feliz"
