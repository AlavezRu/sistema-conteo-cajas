# Envio de cada caja al servidor Flask por HTTP POST en formato JSON.
# Se usa socket con tiempo limite para que el ESP32 no se quede colgado si la compu no contesta.
import socket

RUTA = '/api/caja'


def codigo_http(respuesta):
    """Saca el codigo de la primera linea de la respuesta: b'HTTP/1.1 201 CREATED' -> 201."""
    try:
        return int(respuesta.split(b' ')[1])
    except (IndexError, ValueError):
        return None


def enviar_caja(ip, puerto, token, color, espera_s=5):
    """Manda solo el color y el token; devuelve el codigo HTTP o None si no hubo conexion."""
    cuerpo = '{"color": "%s"}' % color
    peticion = ('POST %s HTTP/1.0\r\n'
                'Host: %s\r\n'
                'Content-Type: application/json\r\n'
                'X-Token-Dispositivo: %s\r\n'
                'Content-Length: %d\r\n\r\n%s') % (RUTA, ip, token, len(cuerpo), cuerpo)
    s = socket.socket()
    s.settimeout(espera_s)  # si el servidor no contesta en ese tiempo, se rinde
    try:
        s.connect(socket.getaddrinfo(ip.strip(), puerto)[0][-1])
        s.send(peticion.encode())
        return codigo_http(s.recv(32))  # el codigo viene al principio de la respuesta
    except OSError as error:
        print('Error al enviar:', error)
        return None
    finally:
        s.close()  # pase lo que pase se cierra, si no el ESP32 se queda sin conexiones
