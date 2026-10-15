# Indicacion local: un LED por color y la pantalla LCD 16x2,
# para que el operador vea el resultado sin necesidad de la computadora.
from machine import Pin, SoftI2C
import time

from i2c_lcd import I2cLcd  # libreria de la pantalla (va en el ESP32 junto con lcd_api.py)
import pines

_leds = {
    'ROJO': Pin(pines.LED_ROJO, Pin.OUT),
    'VERDE': Pin(pines.LED_VERDE, Pin.OUT),
    'AZUL': Pin(pines.LED_AZUL, Pin.OUT),
}
for _led in _leds.values():
    _led.value(0)  # todos arrancan apagados

_i2c = SoftI2C(scl=Pin(pines.LCD_SCL), sda=Pin(pines.LCD_SDA), freq=100000)
_lcd = I2cLcd(_i2c, pines.LCD_DIRECCION, 2, 16)  # 2 renglones y 16 columnas
_lcd.clear()
time.sleep(0.1)  # el borrado tarda unos milisegundos, si no se espera se pierden letras


def encender_led(color):
    """Prende el LED del color y apaga los otros; sin caja se apagan los tres."""
    for nombre, led in _leds.items():
        led.value(1 if nombre == color else 0)


def escribir(arriba, abajo=''):
    """Pone una frase en cada renglon sin que se corten entre los dos."""
    _lcd.move_to(0, 0)
    _lcd.putstr('{:<16}'.format(arriba[:16]))  # recorta a 16 letras y rellena con espacios
    _lcd.move_to(0, 1)
    _lcd.putstr('{:<16}'.format(abajo[:16]))  # los espacios borran lo que estaba antes
