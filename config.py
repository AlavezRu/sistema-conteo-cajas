# Configuracion del servidor.
# Todo lo que es secreto o cambia de una computadora a otra se lee de variables
# de entorno (archivo .env), nunca se escribe en el codigo.
import os

from dotenv import load_dotenv

load_dotenv()  # lee el .env si existe; en GitHub Actions no hay .env y no pasa nada

TOKEN_DISPOSITIVO = os.environ.get('TOKEN_DISPOSITIVO', '')  # el ESP32 lo manda con cada caja
CLAVE_ADMIN = os.environ.get('CLAVE_ADMIN', '')  # protege el reinicio del conteo
SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24).hex()  # si falta, una al azar
TAMANO_HISTORIAL = int(os.environ.get('TAMANO_HISTORIAL', '20'))  # cajas que se devuelven en el historial

DEBUG = os.environ.get('FLASK_DEBUG', '0') == '1'  # la depuracion solo se prende a proposito
HOST = os.environ.get('HOST', '0.0.0.0')  # toda la red, para que el ESP32 lo alcance
PUERTO = int(os.environ.get('PUERTO', '5000'))

# Iteracion 4: registro de las cajas en Google Sheets
RUTA_CREDENCIALES_GOOGLE = os.environ.get('RUTA_CREDENCIALES_GOOGLE', 'credenciales.json')
ID_HOJA = os.environ.get('ID_HOJA', '')
