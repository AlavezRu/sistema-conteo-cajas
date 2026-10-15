# Programa principal del ESP32 (MicroPython). Se sube con Thonny junto con
# config.py, pines.py, colores.py, detector_cajas.py, sensor_color.py,
# indicadores.py, wifi.py, cliente_http.py, i2c_lcd.py y lcd_api.py.
import time

import cliente_http
import config
import indicadores
import sensor_color
from colores import clasificar
from detector_cajas import DetectorCajas
from wifi import ConexionWifi

MAX_PENDIENTES = 50  # cajas que se guardan si el servidor no contesta


def mostrar_conteo(detector, pendientes, ultima):
    abajo = 'Total: %d' % detector.total
    if pendientes:
        abajo += ' P:%d' % len(pendientes)  # cajas que faltan por mandar
    indicadores.escribir('Caja: ' + ultima if ultima else 'Esperando caja', abajo)


indicadores.escribir('Conteo de cajas', 'Iniciando...')
sensor_color.iniciar()

wifi = ConexionWifi(config.SSID, config.PASSWORD, config.REINTENTO_WIFI_S)
indicadores.escribir('Conectando', 'WiFi...')
if wifi.esperar(20):
    print('WiFi conectada | IP:', wifi.ip())
    indicadores.escribir('WiFi conectada', wifi.ip())
    time.sleep(2)  # deja ver la IP dos segundos
else:
    print('Sin WiFi, se sigue contando y se reintenta')

detector = DetectorCajas(config.LECTURAS_CONFIRMACION, config.LECTURAS_LIBRE)
pendientes = []  # cajas contadas que todavia no llegan al servidor
ultima = None  # color de la ultima caja contada, para la pantalla
mostrar_conteo(detector, pendientes, ultima)

while True:
    rojo, verde, azul = sensor_color.leer_frecuencias()
    color = clasificar(rojo, verde, azul, config.AIRE, config.TOLERANCIA_AIRE)
    indicadores.encender_led(color)

    contada = detector.procesar(color)
    if contada:  # paso una caja nueva
        ultima = contada
        print('Caja', detector.total, contada)
        if len(pendientes) < MAX_PENDIENTES:
            pendientes.append(contada)
        else:
            print('Demasiadas cajas pendientes, no se guardo la caja', detector.total)
        mostrar_conteo(detector, pendientes, ultima)

    en_linea = wifi.revisar()  # si se cayo la red la vuelve a pedir sin detener el conteo
    if pendientes and en_linea:
        codigo = cliente_http.enviar_caja(config.IP_SERVIDOR, config.PUERTO,
                                          config.TOKEN_DISPOSITIVO, pendientes[0],
                                          config.ESPERA_SERVIDOR_S)
        if codigo is not None:  # el servidor contesto
            if codigo >= 300:  # la rechazo: reintentar no sirve (token o color mal)
                print('El servidor rechazo la caja, codigo', codigo)
            pendientes.pop(0)
            mostrar_conteo(detector, pendientes, ultima)

    time.sleep_ms(config.PAUSA_MS)
