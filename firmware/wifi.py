# Conexion WiFi con reintentos que no detienen el conteo.
import network
import time


class ConexionWifi:
    def __init__(self, ssid, password, reintento_s=5):
        self.ssid = ssid
        self.password = password
        self.reintento_ms = reintento_s * 1000
        self.wlan = network.WLAN(network.STA_IF)  # modo cliente
        self.wlan.active(True)
        self._ultimo_intento = None

    def conectada(self):
        return self.wlan.isconnected()

    def ip(self):
        return self.wlan.ifconfig()[0]

    def esperar(self, segundos=20):
        """Al arrancar: pide la conexion y espera hasta que llegue o se acabe el tiempo."""
        self._pedir()
        for _ in range(segundos):
            if self.wlan.isconnected():
                return True
            time.sleep(1)
        return self.wlan.isconnected()

    def revisar(self):
        """En el ciclo principal: si se cayo la red, la vuelve a pedir cada reintento_s segundos."""
        if self.wlan.isconnected():
            return True
        ahora = time.ticks_ms()
        if self._ultimo_intento is None or time.ticks_diff(ahora, self._ultimo_intento) >= self.reintento_ms:
            self._pedir()
        return False

    def _pedir(self):
        self._ultimo_intento = time.ticks_ms()
        try:
            self.wlan.connect(self.ssid, self.password)  # no bloquea: la conexion llega despues
        except OSError as error:  # el ESP32 da error si ya estaba intentando conectarse
            print('WiFi:', error)
