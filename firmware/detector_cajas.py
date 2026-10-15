# Deteccion del paso de una caja.
# Mientras una caja esta frente al sensor se producen muchas lecturas; aqui se
# decide cuando es una caja nueva para contarla una sola vez.
# Tampoco usa nada del ESP32, asi que se prueba en la compu con pytest.
from colores import COLORES, SIN_CAJA

LIBRE = 'LIBRE'  # no hay caja contada enfrente, listo para la siguiente
CONFIRMANDO = 'CONFIRMANDO'  # aparecio un color y se espera a que se repita
OCUPADO = 'OCUPADO'  # la caja ya se conto, se espera a que se retire


class DetectorCajas:
    def __init__(self, confirmaciones=3, lecturas_libre=2):
        self.confirmaciones = confirmaciones  # lecturas iguales seguidas para contar
        self.lecturas_libre = lecturas_libre  # lecturas sin caja seguidas para liberar
        self.total = 0
        self.por_color = {color: 0 for color in COLORES}
        self.estado = LIBRE
        self._candidato = None  # color que se esta confirmando
        self._repeticiones = 0  # cuantas lecturas seguidas lleva

    def procesar(self, color):
        """Recibe la lectura mas reciente; devuelve el color si se conto una caja, si no None."""
        if self.estado == OCUPADO:
            if color == SIN_CAJA:
                self._repeticiones += 1
                if self._repeticiones >= self.lecturas_libre:  # la caja ya se fue
                    self._cambiar_a(LIBRE)
            else:
                self._repeticiones = 0  # sigue habiendo algo enfrente
            return None

        if color not in COLORES:  # sin caja o color desconocido: se pierde la racha
            self._cambiar_a(LIBRE)
            return None

        if color == self._candidato:
            self._repeticiones += 1
        else:  # aparecio un color nuevo, se empieza a confirmar desde cero
            self._candidato = color
            self._repeticiones = 1
            self.estado = CONFIRMANDO

        if self._repeticiones >= self.confirmaciones:  # el color ya se repitio lo suficiente
            self.total += 1
            self.por_color[color] += 1
            self._cambiar_a(OCUPADO)
            return color
        return None

    def _cambiar_a(self, estado):
        self.estado = estado
        self._candidato = None
        self._repeticiones = 0
