# Revisión antes de entregar

Esta es una propuesta implementada y publicada como versión base en
[GitHub](https://github.com/JesUsDavIdd/sistema-reservas-hotel).
La publicación no acredita por sí sola los aportes de desarrollo de ambos integrantes.

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
| Casos normales y excepcionales | main.py y test_hotel.py. |
| UML y decisiones de diseño | UML.md, UML.svg y DECISIONES_DISENO.md. |
| README | README.md. |
| Un commit de desarrollo por integrante | Pendiente de realizar por cada integrante. |
| Enlace al repositorio | https://github.com/JesUsDavIdd/sistema-reservas-hotel |

## Trabajo real sugerido

1. Jesús revisa y explica `Hotel`, las reservas y las excepciones. Puede implementar una consulta
   de reservas activas y demostrar que las canceladas no aparecen, con una prueba propia.
2. Juan José revisa y explica las habitaciones y las tarifas. Puede implementar una consulta de
   habitaciones disponibles para un intervalo, utilizando la regla de cruces existente y comprobando
   casos de salida y entrada el mismo día.
3. Cada uno realiza sus cambios desde su cuenta, describe lo que hizo y abre su pull request.
   No crear commits vacíos ni atribuir a otra persona cambios preparados sin su participación.
4. Ambos ejecutan `python main.py` y `python -m unittest -v`, revisan el UML y actualizan las decisiones
   de diseño con sus cambios y aprendizajes reales.
5. Integrar los aportes en el repositorio público del hotel y compartir su enlace para la entrega.

Estos dos cambios son propuestas pendientes, no funciones incluidas en esta versión.

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
