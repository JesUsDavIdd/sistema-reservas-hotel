# Revisión antes de entregar

El proyecto está implementado y publicado con los cambios integrados en
[GitHub](https://github.com/JesUsDavIdd/sistema-reservas-hotel).

## Requisitos localizados

| Requisito del documento | Ubicación |
|---|---|
| Contexto diferente | Reservas de hotel; confirmar que el docente no lo haya usado. |
| Al menos seis clases concretas | Individual, Doble, Suite, Cliente, Reserva, DetalleEstadia y Hotel. |
| Una abstracta y tres hijas | Habitacion, Individual, Doble y Suite en habitaciones.py. |
| Constructores y encapsulamiento | Constructores, atributos internos, propiedades y actualizaciones validadas. |
| Dos métodos sobrescritos en cada hija | calcular_tarifa y mostrar_informacion. |
| Colección heterogénea, un ciclo sin condicionales por tipo | Lista habitaciones y primer for de main.py. |
| Dos relaciones | Reserva con Cliente y con Habitacion. |
| Composición | Reserva construye su DetalleEstadia. |
| Tres excepciones lanzadas y capturadas | excepciones.py; Hotel y DetalleEstadia; tres bloques try/except de main.py. |
| Ocho objetos o más | Solo hotel, tres habitaciones, tres clientes y tres reservas ya suman diez; los detalles son adicionales. |
| Casos normales y excepcionales | main.py. |
| UML y decisiones de diseño | UML.md, UML.svg y DECISIONES_DISENO.md. |
| README | README.md. |
| Un commit de desarrollo por integrante | Aporte de Juan José en PR #1 y cambio solicitado por Jesús en el historial de main. |
| Enlace al repositorio | https://github.com/JesUsDavIdd/sistema-reservas-hotel |

## Cambios integrados

- Juan José envió la consulta de habitaciones disponibles en el
  [pull request #1](https://github.com/JesUsDavIdd/sistema-reservas-hotel/pull/1).
- Desde la cuenta de Jesús se publicó la consulta de reservas activas, la corrección de la comparación
  de fechas y la actualización del programa principal y la documentación. Ese cambio se preparó
  con apoyo de Codex, según lo indicado en las decisiones de diseño.

El [historial](https://github.com/JesUsDavIdd/sistema-reservas-hotel/commits/main/)
conserva ambos cambios. Para revisar la versión integrada, ejecutar `python main.py` y contrastar
los resultados con los métodos descritos en el UML.

## Preguntas para comprobar la comprensión

- ¿Por qué no se puede crear una instancia de Habitacion?
- ¿Qué dos métodos cambian en las tres hijas y qué dato propio usa cada una?
- ¿Por qué una reserva se asocia con la habitación pero contiene su detalle?
- ¿Por qué se permite otra entrada el día de salida?
- ¿Dónde se lanza cada excepción y cómo continúa el programa?
- ¿Por qué una actualización de tarifa no cambia el precio de una reserva existente?

El documento exige declarar el uso de IA. Conservar una declaración fiel al apoyo recibido y registrar
los cambios que ustedes hagan. Confirmar también la fecha de cierre en la plataforma: los datos
compartidos muestran tanto 1 como 8 de noviembre de 2026.
