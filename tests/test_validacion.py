import pytest

from validacion import token_valido, validar_caja


@pytest.mark.parametrize('enviado, esperado', [
    ('ROJO', 'ROJO'),
    ('verde', 'VERDE'),
    (' Azul ', 'AZUL'),
])
def test_acepta_los_tres_colores(enviado, esperado):
    assert validar_caja({'color': enviado}) == (esperado, None)


@pytest.mark.parametrize('datos', [
    None,
    'ROJO',
    [],
    {},
    {'colour': 'ROJO'},
    {'color': 5},
    {'color': 'NEGRO'},
    {'color': 'SIN CAJA'},
    {'color': ''},
])
def test_rechaza_datos_invalidos(datos):
    color, error = validar_caja(datos)
    assert color is None
    assert error


def test_token_correcto():
    assert token_valido('abc123', 'abc123')


@pytest.mark.parametrize('recibido, esperado', [
    ('', 'abc123'),
    ('abc124', 'abc123'),
    ('abc123', ''),  # servidor sin token configurado: no acepta nada
    ('', ''),
])
def test_token_incorrecto(recibido, esperado):
    assert not token_valido(recibido, esperado)
