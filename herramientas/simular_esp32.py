# Corre firmware/main.py en la computadora, sin la tarjeta, para probar el flujo completo:
# sensor simulado -> deteccion del paso de la caja -> envio HTTP -> servidor Flask.
# El sensor, el WiFi, los LEDs y la pantalla se reemplazan por imitaciones;
# el envio de las cajas al servidor es real.
#
# Uso (con el servidor corriendo y el mismo token del .env):
#   python herramientas/simular_esp32.py 127.0.0.1 5000 el-token-del-env
import os
import runpy
import sys
import time
import types

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IP, PUERTO, TOKEN = sys.argv[1], int(sys.argv[2]), sys.argv[3]
sys.path.insert(0, os.path.join(RAIZ, 'firmware'))

# funciones de tiempo que MicroPython tiene y la computadora no
time.ticks_ms = lambda: int(time.monotonic() * 1000)
time.ticks_us = lambda: int(time.monotonic() * 1_000_000)
time.ticks_diff = lambda a, b: a - b
time.sleep_ms = lambda ms: None
time.sleep = lambda s: None  # sin esperas en la simulacion


class Pin:
    OUT, IN = 1, 0

    def __init__(self, numero, modo=None):
        self.v = 0

    def value(self, v=None):
        if v is None:
            return self.v
        self.v = v


class WLAN:
    def __init__(self, interfaz):
        self.conectada = False

    def active(self, activa):
        pass

    def connect(self, ssid, password):
        self.conectada = True

    def isconnected(self):
        return self.conectada

    def ifconfig(self):
        return ('192.168.1.50',)


class I2cLcd:
    """Imprime en la consola lo que mostraria la pantalla."""

    def __init__(self, *args):
        self.renglones = ['', '']
        self.fila = 0

    def clear(self):
        pass

    def move_to(self, columna, fila):
        self.fila = fila

    def putstr(self, texto):
        self.renglones[self.fila] = texto
        if self.fila == 1:
            print('   LCD |%s|%s|' % tuple(self.renglones))


AIRE = (15100, 13150, 13150)
ROJO, VERDE, AZUL = (9000, 3000, 3500), (3000, 9000, 3500), (3000, 3500, 9000)
# cuatro cajas: cada una se queda varias lecturas frente al sensor
LECTURAS = ([AIRE] * 2 + [ROJO] * 6 + [AIRE] * 3 + [AZUL] * 5 + [AIRE] * 3
            + [ROJO] * 4 + [AIRE] * 3 + [VERDE] * 7 + [AIRE] * 4)


class FinDeLecturas(Exception):
    pass


def leer_frecuencias(lecturas=iter(LECTURAS)):
    try:
        return next(lecturas)
    except StopIteration:
        raise FinDeLecturas


def modulo(nombre, **contenido):
    m = types.ModuleType(nombre)
    m.__dict__.update(contenido)
    sys.modules[nombre] = m
    return m


modulo('machine', Pin=Pin, SoftI2C=lambda **k: None)
modulo('network', WLAN=WLAN, STA_IF=0)
modulo('i2c_lcd', I2cLcd=I2cLcd)
modulo('sensor_color', iniciar=lambda: None, leer_frecuencias=leer_frecuencias)

config = modulo('config')
with open(os.path.join(RAIZ, 'firmware', 'config_ejemplo.py'), encoding='utf-8') as f:
    exec(f.read(), config.__dict__)
config.IP_SERVIDOR, config.PUERTO, config.TOKEN_DISPOSITIVO = IP, PUERTO, TOKEN

try:
    runpy.run_path(os.path.join(RAIZ, 'firmware', 'main.py'), run_name='__main__')
except FinDeLecturas:
    print('Fin de la simulacion')
