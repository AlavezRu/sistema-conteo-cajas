# Sistema Web de Conteo de Cajas por Color

Proyecto de la asignatura **Desarrollo de Aplicaciones Web (DSB2501)**, Instituto Tecnológico Superior de Teposcolula.

Un ESP32 con sensor de color TCS3200 identifica cada caja que pasa frente al sensor, la cuenta una sola vez y la manda a un servidor Flask, que valida la caja y lleva el conteo total y por color. En las siguientes iteraciones cada caja se registrará en la API de Google Sheets y el conteo se verá en una página web que se actualiza sola.

Es la parte de software del proyecto **Clasificador de Cajas por Color** de Sistemas Programables.

**Equipo:** Mario Ruiz Alavez y Julio César Ortiz Hernández
**Docente:** Daniel García Zanabria

## Estado por iteración

| Iteración | Fechas | Entregable | Estado |
|---|---|---|---|
| 1 | 28 sep – 2 oct | Repositorio, configuración segura y plan de entregas | `v0.1` |
| 2 | 5 – 9 oct | Firmware del ESP32 contando cajas | `v0.2` (falta probar en la tarjeta) |
| 3 | 12 – 16 oct | API de conteo validada con pruebas | En curso |
| 4 | 19 – 23 oct | Cajas registradas en Google Sheets | Pendiente |
| 5 | 26 – 30 oct | Interfaz web con inicio de sesión | Pendiente |
| 6 | 2 – 6 nov | Versión 1.0, documentación y manual | Pendiente |

Las historias de usuario están en [docs/historias_usuario.md](docs/historias_usuario.md).

## Estructura

```
├── Pagina.py              servidor Flask: rutas de la API
├── conteo.py              lógica del conteo total y por color
├── validacion.py          token del dispositivo y validación de cada caja
├── config.py              lee la configuración del archivo .env
├── .env.ejemplo           variables que hay que crear en el .env
├── requirements.txt       dependencias del servidor
├── firmware/              programa del ESP32 en MicroPython
│   ├── main.py            ciclo principal
│   ├── config_ejemplo.py  plantilla de config.py (WiFi, servidor, token, calibración)
│   ├── pines.py           asignación de pines
│   ├── wifi.py            conexión WiFi con reintentos
│   ├── sensor_color.py    lectura de frecuencias del TCS3200
│   ├── colores.py         identificación del color (ROJO, VERDE, AZUL)
│   ├── detector_cajas.py  detección del paso de la caja
│   ├── indicadores.py     LEDs y pantalla LCD
│   └── cliente_http.py    envío de cada caja al servidor
├── tests/                 pruebas con pytest
└── .github/workflows/     GitHub Actions corre las pruebas en cada push y pull request
```

## Servidor

Requiere Python 3.10 o superior.

```bash
python -m venv .venv
.venv\Scripts\activate          # en Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.ejemplo .env          # en Linux: cp .env.ejemplo .env
python Pagina.py
```

Cambia los valores del `.env` antes de usarlo. El `.env` y `credenciales.json` nunca se suben al repositorio.

### API

| Método | Ruta | Qué hace | Protección |
|---|---|---|---|
| POST | `/api/caja` | Recibe `{"color": "ROJO"}` y cuenta la caja | Encabezado `X-Token-Dispositivo` |
| GET | `/api/conteo` | Total, conteo por color, última caja e historial | — |
| POST | `/api/reiniciar` | Deja el conteo en cero | Encabezado `X-Clave-Admin` |

Respuestas: `201` caja contada, `400` JSON incompleto o color no reconocido, `401` sin token o clave válidos.

## Firmware del ESP32

1. Instala el firmware de MicroPython en el ESP32 y abre Thonny con el intérprete *MicroPython (ESP32)*.
2. Copia `firmware/config_ejemplo.py` como `config.py` y llena la red WiFi, la IP de la computadora del servidor y el mismo `TOKEN_DISPOSITIVO` del `.env`.
3. Sube al ESP32 todos los archivos de `firmware/`, tu `config.py` y las librerías de la pantalla `i2c_lcd.py` y `lcd_api.py`.
4. Para calibrar, corre el programa sin nada enfrente del sensor y copia la lectura en `AIRE` dentro de `config.py`.

Una caja se cuenta cuando el mismo color aparece en 3 lecturas seguidas, y no se vuelve a contar hasta que el sensor queda libre. Si el servidor no contesta, las cajas se guardan y se mandan cuando vuelve la conexión.

## Pruebas

```bash
pytest -v
```

Se prueban la validación, el conteo, las rutas de la API y la lógica del firmware que no depende de la tarjeta (identificación del color y paso de la caja).
