from datetime import datetime

import pytest

from conteo import Conteo


def test_empieza_en_cero():
    resumen = Conteo().resumen()
    assert resumen['total'] == 0
    assert resumen['por_color'] == {'ROJO': 0, 'VERDE': 0, 'AZUL': 0}
    assert resumen['ultima'] is None
    assert resumen['historial'] == []


def test_cuenta_total_y_por_color():
    conteo = Conteo()
    for color in ['ROJO', 'VERDE', 'ROJO', 'AZUL', 'ROJO']:
        conteo.registrar(color)
    resumen = conteo.resumen()
    assert resumen['total'] == 5
    assert resumen['por_color'] == {'ROJO': 3, 'VERDE': 1, 'AZUL': 1}


def test_numero_consecutivo_fecha_y_hora():
    conteo = Conteo()
    conteo.registrar('ROJO')
    caja = conteo.registrar('AZUL', momento=datetime(2026, 10, 14, 9, 30, 5))
    assert caja == {'numero': 2, 'fecha': '14/10/2026', 'hora': '09:30:05', 'color': 'AZUL'}


def test_historial_con_la_mas_reciente_primero():
    conteo = Conteo(tamano_historial=3)
    for color in ['ROJO', 'VERDE', 'AZUL', 'VERDE']:
        conteo.registrar(color)
    resumen = conteo.resumen()
    assert [caja['numero'] for caja in resumen['historial']] == [4, 3, 2]  # la 1 ya salio
    assert resumen['ultima']['numero'] == 4
    assert resumen['total'] == 4  # el historial se recorta, el total no


def test_no_cuenta_colores_desconocidos():
    conteo = Conteo()
    with pytest.raises(ValueError):
        conteo.registrar('NEGRO')
    assert conteo.resumen()['total'] == 0


def test_reiniciar_deja_todo_en_cero():
    conteo = Conteo()
    conteo.registrar('ROJO')
    conteo.registrar('VERDE')
    conteo.reiniciar()
    assert conteo.resumen() == Conteo().resumen()
    assert conteo.registrar('AZUL')['numero'] == 1
