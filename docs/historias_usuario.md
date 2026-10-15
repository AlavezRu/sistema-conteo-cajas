# Historias de usuario

Plan de entregas del reporte C2-A1-P1. Cada historia se registra como issue en GitHub.

| Clave | Iteración | Historia de usuario | Prioridad | Estado |
|---|---|---|---|---|
| HU-01 | 1 | Como equipo, quiero un repositorio en GitHub con la configuración sensible fuera del código para trabajar en conjunto sin exponer credenciales. | Alta | Terminada |
| HU-02 | 2 | Como operador, quiero que el ESP32 identifique el color de cada caja y lo indique en un LED y en el LCD. | Alta | Falta probar en la tarjeta |
| HU-03 | 2 | Como operador, quiero que cada caja se cuente una sola vez aunque se quede unos segundos frente al sensor. | Alta | Falta probar en la tarjeta |
| HU-04 | 3 | Como sistema, quiero recibir y validar las cajas enviadas por el ESP32 autorizado para no contar datos falsos. | Alta | En curso |
| HU-05 | 4 | Como supervisor, quiero que cada caja quede registrada en la API de Google Sheets con su número, fecha, hora y color. | Alta | Pendiente |
| HU-06 | 4 | Como supervisor, quiero que el conteo no se pierda si la API de Google Sheets no responde o si el servidor se reinicia. | Media | Pendiente |
| HU-07 | 5 | Como supervisor, quiero ver en el navegador el total de cajas y cuántas hay de cada color, y que la página se actualice sola. | Alta | Pendiente |
| HU-08 | 5 | Como administrador, quiero que solo un usuario autenticado pueda reiniciar el conteo. | Alta | Pendiente |
| HU-09 | 6 | Como docente, quiero un manual de usuario y una documentación técnica para instalar y operar el sistema. | Media | Pendiente |

## Definición de terminado

Una historia está terminada cuando su código está en la rama `main`, sus pruebas
pasan en GitHub Actions, funciona con el hardware real y no mete secretos al repositorio.
