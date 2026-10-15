# Validacion de lo que llega al servidor: el token del ESP32 y el JSON de cada caja.
import hmac

from conteo import COLORES


def token_valido(recibido, esperado):
    """Compara el token sin revelar, por el tiempo que tarda, cuantas letras coinciden."""
    if not esperado or not recibido:  # si el servidor no tiene token configurado no acepta nada
        return False
    return hmac.compare_digest(recibido.encode(), esperado.encode())


def validar_caja(datos):
    """Devuelve (color, None) si la caja esta bien, o (None, mensaje) si no."""
    if not isinstance(datos, dict):
        return None, 'Se esperaba un objeto JSON'
    color = datos.get('color')
    if color is None:
        return None, 'Falta el campo color'
    if not isinstance(color, str):
        return None, 'El color debe ser texto'
    color = color.strip().upper()
    if color not in COLORES:
        return None, 'Color no reconocido; solo se acepta ' + ', '.join(COLORES)
    return color, None
