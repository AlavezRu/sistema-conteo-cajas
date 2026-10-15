# Lectura del sensor TCS3200: mide la frecuencia de los canales rojo, verde y azul.
from machine import Pin
import time

import pines

S0 = Pin(pines.SENSOR_S0, Pin.OUT)
S1 = Pin(pines.SENSOR_S1, Pin.OUT)
S2 = Pin(pines.SENSOR_S2, Pin.OUT)
S3 = Pin(pines.SENSOR_S3, Pin.OUT)
OUT = Pin(pines.SENSOR_OUT, Pin.IN)


def iniciar():
    """Pone la escala de frecuencia del sensor al 100%."""
    S0.value(1)
    S1.value(1)


def medir_frecuencia(tiempo_medicion=150):
    """Cuenta los pulsos de OUT durante tiempo_medicion milisegundos y devuelve los Hz."""
    contador = 0
    estado_anterior = OUT.value()
    tiempo_inicio = time.ticks_us()  # microsegundos para una mejor precision del tiempo
    tiempo_total_us = tiempo_medicion * 1000
    while time.ticks_diff(time.ticks_us(), tiempo_inicio) < tiempo_total_us:
        estado_actual = OUT.value()
        if estado_actual == 1 and estado_anterior == 0:  # flanco de subida: un pulso
            contador += 1
        estado_anterior = estado_actual
    return contador * (1_000_000 / tiempo_total_us)  # un segundo tiene 1 000 000 de microsegundos


def leer_frecuencias():
    """Devuelve (rojo, verde, azul) en Hz."""
    S2.value(0)  # filtro rojo: S2=0, S3=0
    S3.value(0)
    time.sleep_ms(30)  # tiempo para que se acomode el filtro
    rojo = medir_frecuencia()

    S2.value(1)  # filtro verde: S2=1, S3=1
    S3.value(1)
    time.sleep_ms(30)
    verde = medir_frecuencia()

    S2.value(0)  # filtro azul: S2=0, S3=1
    S3.value(1)
    time.sleep_ms(30)
    azul = medir_frecuencia()
    return rojo, verde, azul
