# Pruebas de la logica del firmware que no depende del ESP32:
# la identificacion del color y la deteccion del paso de la caja.
from colores import DESCONOCIDO, SIN_CAJA, clasificar
from detector_cajas import LIBRE, OCUPADO, DetectorCajas

AIRE = (15100, 13150, 13150)  # calibracion de la practica del 22 de septiembre


def test_sensor_al_aire_es_sin_caja():
    assert clasificar(15100, 13150, 13150, AIRE) == SIN_CAJA
    assert clasificar(15800, 12600, 13700, AIRE) == SIN_CAJA  # dentro del 10%


def test_canal_dominante_da_el_color():
    assert clasificar(9000, 3000, 3500, AIRE) == 'ROJO'
    assert clasificar(3000, 9000, 3500, AIRE) == 'VERDE'
    assert clasificar(3000, 3500, 9000, AIRE) == 'AZUL'


def test_canales_parejos_no_son_caja_de_color():
    assert clasificar(5000, 4800, 4900, AIRE) == SIN_CAJA


def test_negro_y_empates_son_desconocidos():
    assert clasificar(10, 12, 8, AIRE) == DESCONOCIDO
    assert clasificar(9000, 9000, 2000, AIRE) == DESCONOCIDO


def pasar(detector, lecturas):
    """Procesa varias lecturas y devuelve las cajas que se contaron."""
    return [color for color in map(detector.procesar, lecturas) if color]


def test_una_caja_frente_al_sensor_se_cuenta_una_vez():
    detector = DetectorCajas(confirmaciones=3)
    contadas = pasar(detector, [SIN_CAJA] + ['ROJO'] * 20 + [SIN_CAJA] * 2)
    assert contadas == ['ROJO']
    assert detector.total == 1


def test_necesita_tres_lecturas_iguales():
    detector = DetectorCajas(confirmaciones=3)
    assert pasar(detector, ['VERDE', 'VERDE']) == []
    assert detector.procesar('VERDE') == 'VERDE'


def test_una_lectura_suelta_no_cuenta():
    detector = DetectorCajas(confirmaciones=3)
    assert pasar(detector, ['AZUL', SIN_CAJA, 'AZUL', 'AZUL', SIN_CAJA]) == []
    assert detector.total == 0


def test_cambio_de_color_reinicia_la_confirmacion():
    detector = DetectorCajas(confirmaciones=3)
    assert pasar(detector, ['ROJO', 'ROJO', 'VERDE', 'VERDE']) == []
    assert detector.procesar('VERDE') == 'VERDE'


def test_no_cuenta_otra_hasta_que_el_sensor_queda_libre():
    detector = DetectorCajas(confirmaciones=3, lecturas_libre=2)
    pasar(detector, ['ROJO'] * 3)
    assert detector.estado == OCUPADO
    # una sola lectura libre o un color desconocido no liberan el sensor
    assert pasar(detector, [SIN_CAJA, DESCONOCIDO, 'ROJO', 'ROJO', 'ROJO']) == []
    pasar(detector, [SIN_CAJA, SIN_CAJA])
    assert detector.estado == LIBRE


def test_varias_cajas_seguidas():
    detector = DetectorCajas(confirmaciones=3, lecturas_libre=2)
    libre = [SIN_CAJA] * 2
    lecturas = ['ROJO'] * 5 + libre + ['AZUL'] * 4 + libre + ['ROJO'] * 3 + libre + ['VERDE'] * 6 + libre
    assert pasar(detector, lecturas) == ['ROJO', 'AZUL', 'ROJO', 'VERDE']
    assert detector.total == 4
    assert detector.por_color == {'ROJO': 2, 'VERDE': 1, 'AZUL': 1}
