# Servidor Flask del Sistema Web de Conteo de Cajas por Color.
# Iteracion 3: API que recibe las cajas del ESP32 y calcula el conteo.
# La pagina con el conteo (index.html) llega en la iteracion 5.
from flask import Flask, jsonify, request

import config
from conteo import Conteo
from validacion import token_valido, validar_caja


def crear_app(**ajustes):
    """Arma la aplicacion; las pruebas mandan sus propios tokens en ajustes."""
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=config.SECRET_KEY,
        TOKEN_DISPOSITIVO=config.TOKEN_DISPOSITIVO,
        CLAVE_ADMIN=config.CLAVE_ADMIN,
        TAMANO_HISTORIAL=config.TAMANO_HISTORIAL,
    )
    app.config.update(ajustes)
    conteo = Conteo(app.config['TAMANO_HISTORIAL'])

    @app.post('/api/caja')  # el ESP32 manda aqui cada caja que detecta
    def recibir_caja():
        token = request.headers.get('X-Token-Dispositivo', '')
        if not token_valido(token, app.config['TOKEN_DISPOSITIVO']):
            app.logger.warning('Caja rechazada: token no valido desde %s', request.remote_addr)
            return jsonify({'ok': False, 'error': 'Token de dispositivo no valido'}), 401

        color, error = validar_caja(request.get_json(silent=True))
        if error:
            return jsonify({'ok': False, 'error': error}), 400

        caja = conteo.registrar(color)
        return jsonify({'ok': True, 'caja': caja}), 201

    @app.get('/api/conteo')  # total, conteo por color, ultima caja e historial
    def consultar_conteo():
        return jsonify({'ok': True, **conteo.resumen()})

    @app.post('/api/reiniciar')  # deja el conteo en cero; solo con la clave de administrador
    def reiniciar_conteo():
        clave = request.headers.get('X-Clave-Admin', '')
        if not token_valido(clave, app.config['CLAVE_ADMIN']):
            app.logger.warning('Reinicio rechazado desde %s', request.remote_addr)
            return jsonify({'ok': False, 'error': 'No autorizado'}), 401
        conteo.reiniciar()
        app.logger.warning('Conteo reiniciado desde %s', request.remote_addr)
        return jsonify({'ok': True, **conteo.resumen()})

    return app


app = crear_app()

if __name__ == '__main__':
    if not config.TOKEN_DISPOSITIVO:
        print('OJO: falta TOKEN_DISPOSITIVO en el .env, no se aceptara ninguna caja')
    app.run(host=config.HOST, port=config.PUERTO, debug=config.DEBUG)
