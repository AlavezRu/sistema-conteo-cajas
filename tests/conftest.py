import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
# colores.py y detector_cajas.py no dependen del ESP32, asi que se prueban aqui;
# va al final para que el config.py del firmware no tape al del servidor
sys.path.append(os.path.join(RAIZ, 'firmware'))

from Pagina import crear_app  # noqa: E402

TOKEN = 'token-de-prueba'
CLAVE = 'clave-de-prueba'


@pytest.fixture
def cliente():
    app = crear_app(TESTING=True, TOKEN_DISPOSITIVO=TOKEN, CLAVE_ADMIN=CLAVE)
    return app.test_client()
