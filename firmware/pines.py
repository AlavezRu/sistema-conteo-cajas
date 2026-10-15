# Asignacion de pines del ESP32.
# Es la misma conexion de la practica del sensor TCS3200 que ya funciona;
# si cambia el cableado, solo se cambia aqui.

# Sensor de color TCS3200 (GY-31)
SENSOR_S0 = 5
SENSOR_S1 = 18
SENSOR_S2 = 19
SENSOR_S3 = 21
SENSOR_OUT = 22  # el sensor manda la senal por aqui, por eso va como entrada

# Pantalla LCD 16x2 con adaptador I2C
# no se usan los pines 21 y 22 como en otros proyectos porque ahi esta el sensor
LCD_SDA = 32
LCD_SCL = 33
LCD_DIRECCION = 0x27

# LEDs indicadores, uno por color
LED_ROJO = 25
LED_VERDE = 26
LED_AZUL = 27
