# Copia este archivo como config.py, llena tus datos y subelo al ESP32 con Thonny.
# config.py NO se sube a GitHub (esta en .gitignore) porque lleva la contrasena
# del WiFi y el token del dispositivo.

# Red WiFi
SSID = 'nombre-de-tu-red'
PASSWORD = 'contrasena-de-tu-red'
REINTENTO_WIFI_S = 5  # si se cae el WiFi, se vuelve a intentar cada 5 segundos

# Servidor Flask (la compu donde corre Pagina.py)
IP_SERVIDOR = '192.168.1.100'  # sin espacios
PUERTO = 5000
TOKEN_DISPOSITIVO = 'el-mismo-token-que-en-el-env-del-servidor'
ESPERA_SERVIDOR_S = 5  # segundos que se espera al servidor antes de rendirse

# Calibracion del sensor: lectura con el sensor viendo al aire, sin caja (R, G, B en Hz)
# corre el programa sin poner nada enfrente y copia aqui los tres numeros que salgan
AIRE = (15100, 13150, 13150)
TOLERANCIA_AIRE = 0.10  # si los tres quedan a menos del 10% de esos valores, no hay caja

# Deteccion del paso de la caja
LECTURAS_CONFIRMACION = 3  # lecturas seguidas del mismo color para contar una caja
LECTURAS_LIBRE = 2  # lecturas seguidas sin caja para quedar listo para la siguiente
PAUSA_MS = 100  # pausa entre lecturas
