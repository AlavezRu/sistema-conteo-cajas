from conftest import CLAVE, TOKEN


def enviar(cliente, datos, token=TOKEN):
    encabezados = {'X-Token-Dispositivo': token} if token is not None else {}
    return cliente.post('/api/caja', json=datos, headers=encabezados)


def total(cliente):
    return cliente.get('/api/conteo').get_json()['total']


def test_consulta_inicial_en_cero(cliente):
    respuesta = cliente.get('/api/conteo')
    assert respuesta.status_code == 200
    datos = respuesta.get_json()
    assert datos['total'] == 0
    assert datos['por_color'] == {'ROJO': 0, 'VERDE': 0, 'AZUL': 0}


def test_recibe_una_caja_valida(cliente):
    respuesta = enviar(cliente, {'color': 'ROJO'})
    assert respuesta.status_code == 201
    caja = respuesta.get_json()['caja']
    assert caja['numero'] == 1
    assert caja['color'] == 'ROJO'

    datos = cliente.get('/api/conteo').get_json()
    assert datos['total'] == 1
    assert datos['por_color']['ROJO'] == 1
    assert datos['ultima']['color'] == 'ROJO'


def test_rechaza_caja_sin_token(cliente):
    assert enviar(cliente, {'color': 'ROJO'}, token=None).status_code == 401
    assert total(cliente) == 0


def test_rechaza_caja_con_token_equivocado(cliente):
    assert enviar(cliente, {'color': 'ROJO'}, token='otro-token').status_code == 401
    assert total(cliente) == 0


def test_rechaza_color_no_reconocido(cliente):
    respuesta = enviar(cliente, {'color': 'MORADO'})
    assert respuesta.status_code == 400
    assert respuesta.get_json()['ok'] is False
    assert total(cliente) == 0


def test_rechaza_peticion_sin_json(cliente):
    respuesta = cliente.post('/api/caja', data='ROJO', headers={'X-Token-Dispositivo': TOKEN})
    assert respuesta.status_code == 400


def test_conteo_por_color_con_varias_cajas(cliente):
    for color in ['ROJO', 'VERDE', 'VERDE', 'AZUL', 'AZUL', 'AZUL']:
        enviar(cliente, {'color': color})
    datos = cliente.get('/api/conteo').get_json()
    assert datos['total'] == 6
    assert datos['por_color'] == {'ROJO': 1, 'VERDE': 2, 'AZUL': 3}
    assert [caja['numero'] for caja in datos['historial']] == [6, 5, 4, 3, 2, 1]


def test_reiniciar_sin_clave_no_borra_nada(cliente):
    enviar(cliente, {'color': 'VERDE'})
    assert cliente.post('/api/reiniciar').status_code == 401
    assert cliente.post('/api/reiniciar', headers={'X-Clave-Admin': 'adivinada'}).status_code == 401
    assert total(cliente) == 1


def test_reiniciar_con_clave_deja_en_cero(cliente):
    enviar(cliente, {'color': 'VERDE'})
    respuesta = cliente.post('/api/reiniciar', headers={'X-Clave-Admin': CLAVE})
    assert respuesta.status_code == 200
    assert respuesta.get_json()['total'] == 0
    assert total(cliente) == 0


def test_el_reinicio_solo_acepta_post(cliente):
    assert cliente.get('/api/reiniciar').status_code == 405
