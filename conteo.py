# Logica del conteo de cajas: el total, un contador por color,
# la ultima caja y el historial de las mas recientes.
# En la iteracion 4 cada caja tambien se guardara en Google Sheets.
import threading
from collections import deque
from datetime import datetime

COLORES = ('ROJO', 'VERDE', 'AZUL')  # los unicos colores que cuenta el sistema


class Conteo:
    def __init__(self, tamano_historial=20):
        self._candado = threading.Lock()  # Flask puede atender varias peticiones a la vez
        self._tamano_historial = tamano_historial
        self.reiniciar()

    def reiniciar(self):
        """Deja todos los contadores en cero."""
        with self._candado:
            self._total = 0
            self._por_color = {color: 0 for color in COLORES}
            self._historial = deque(maxlen=self._tamano_historial)  # las mas viejas se van solas

    def registrar(self, color, momento=None):
        """Cuenta una caja y devuelve su registro con numero consecutivo, fecha, hora y color."""
        if color not in COLORES:
            raise ValueError(f'Color no valido: {color}')
        momento = momento or datetime.now()
        with self._candado:
            self._total += 1
            self._por_color[color] += 1
            caja = {
                'numero': self._total,
                'fecha': momento.strftime('%d/%m/%Y'),
                'hora': momento.strftime('%H:%M:%S'),
                'color': color,
            }
            self._historial.appendleft(caja)  # la mas reciente queda primero
        return caja

    def resumen(self):
        """Total, conteo por color, ultima caja e historial."""
        with self._candado:
            historial = list(self._historial)
            return {
                'total': self._total,
                'por_color': dict(self._por_color),
                'ultima': historial[0] if historial else None,
                'historial': historial,
            }
