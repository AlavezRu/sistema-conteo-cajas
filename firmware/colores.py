# Identificacion del color a partir de las tres frecuencias del sensor.
# Las frecuencias solo se usan aqui adentro: no se muestran ni se mandan al servidor.
# Este modulo no usa nada del ESP32, por eso tambien se prueba en la compu con pytest.

COLORES = ('ROJO', 'VERDE', 'AZUL')  # los unicos colores que se cuentan
SIN_CAJA = 'SIN CAJA'  # no hay nada enfrente del sensor
DESCONOCIDO = 'DESCONOCIDO'  # hay algo, pero no es rojo, verde ni azul (negro, mezcla)

UMBRAL_MINIMO = 30  # Hz; si los tres canales quedan abajo, el objeto es negro
UMBRAL_BLANCO = 150  # Hz; si los tres quedan arriba y parejos, no hay un color definido
DIFERENCIA_MINIMA = 0.35  # el canal mayor debe superar al menor por mas del 35%


def es_aire(rojo, verde, azul, aire, tolerancia):
    """Dice si la lectura se parece a la que da el sensor cuando no hay nada enfrente."""
    lectura = (rojo, verde, azul)
    for i in range(3):  # revisa los tres canales uno por uno
        if abs(lectura[i] - aire[i]) > aire[i] * tolerancia:  # si uno se sale del margen
            return False  # entonces si hay algo enfrente
    return True


def clasificar(rojo, verde, azul, aire, tolerancia_aire=0.10):
    """Devuelve ROJO, VERDE, AZUL, SIN CAJA o DESCONOCIDO."""
    if es_aire(rojo, verde, azul, aire, tolerancia_aire):
        return SIN_CAJA

    if rojo < UMBRAL_MINIMO and verde < UMBRAL_MINIMO and azul < UMBRAL_MINIMO:
        return DESCONOCIDO  # casi no regresa luz: objeto negro

    if rojo > UMBRAL_BLANCO and verde > UMBRAL_BLANCO and azul > UMBRAL_BLANCO:
        mayor = max(rojo, verde, azul)
        menor = min(rojo, verde, azul)
        if mayor - menor < mayor * DIFERENCIA_MINIMA:  # los tres canales casi iguales
            return SIN_CAJA  # superficie blanca o sin color: no es una caja de color

    # gana el canal con mas frecuencia
    if rojo > verde and rojo > azul:
        return 'ROJO'
    if verde > rojo and verde > azul:
        return 'VERDE'
    if azul > rojo and azul > verde:
        return 'AZUL'
    return DESCONOCIDO  # empate entre canales: color mezclado
