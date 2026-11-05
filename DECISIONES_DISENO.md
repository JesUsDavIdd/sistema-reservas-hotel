# Documento de Decisiones de Diseño

**Universidad de Manizales**  
**Facultad de Ciencias e Ingenierías**  
**Actividad Colaborativa N.º 3 — Proyecto Final**  
**Sistema de reservas de hotel**

**Integrantes:** Juan Jose Lopera Morales y Jesus David Becerra Tascon.  
**Fecha de preparación:** 2 de noviembre de 2026.  
**Estado:** versión integrada con consultas de disponibilidad y reservas activas.  
**Última actualización:** 4 de noviembre de 2026.

## 1. Introducción

Un hotel necesita conocer qué habitación está reservada y durante qué fechas. Un registro sin control
de cruces puede asignar la misma habitación a dos clientes. El sistema propuesto aborda ese problema
mediante reservas que relacionan clientes, habitaciones y fechas de estancia.

Se utiliza un contexto distinto del sistema académico anterior. Antes de adoptarlo como tema final,
el equipo debe confirmar que el profesor no haya trabajado un hotel durante el módulo, pues el
documento también excluye los contextos usados previamente por el docente.

## 2. Solución y responsabilidades

El alcance se limita a registrar habitaciones, crear y consultar reservas, calcular el precio y cancelar
reservas. Los datos se conservan en memoria. No se incluyen pagos, usuarios, persistencia ni interfaz gráfica.

| Clase | Responsabilidad |
|---|---|
| `Habitacion` | Definir el número, la tarifa base y el contrato común de las habitaciones. |
| `Individual` | Representar una habitación individual y considerar el desayuno en la tarifa. |
| `Doble` | Representar una habitación doble y considerar la cantidad de camas. |
| `Suite` | Representar una suite y considerar el jacuzzi. |
| `Cliente` | Conservar el documento y un nombre válido del huésped. |
| `DetalleEstadia` | Validar fechas, calcular noches y detectar cruces entre estancias. |
| `Reserva` | Unir cliente y habitación con una estancia, conservar la tarifa y controlar la cancelación. |
| `Hotel` | Mantener los registros, evitar reservas incompatibles y consultar reservas activas y habitaciones disponibles. |

Existen siete clases concretas del dominio y una abstracta, sin contar las excepciones.
La responsabilidad de detectar conflictos queda en `Hotel`, porque una reserva aislada no conoce
las demás. Los diccionarios permiten consultar habitaciones y reservas por sus identificadores.
Los listados devuelven tuplas para no exponer directamente los diccionarios internos.

## 3. Abstracción, herencia y encapsulamiento

`Habitacion` hereda de `ABC`. Sus métodos abstractos `calcular_tarifa()` y `mostrar_informacion()`
obligan a que cada especialización proporcione su implementación. No debe instanciarse porque el
sistema necesita conocer un tipo concreto para determinar sus características y su tarifa.

La herencia representa una relación «es una»: una individual, una doble y una suite son habitaciones.
Comparten número, tarifa base, propiedades y actualización validada de la tarifa. Cada hija añade
un dato propio: desayuno, camas o jacuzzi. La especialización se usa tanto al describir la habitación
como al calcular su precio, por lo que no se limita a cambiar el nombre de una clase.

Los constructores establecen datos válidos desde el inicio. Los atributos internos se identifican con
`_`; las propiedades exponen lecturas y métodos como `actualizar_nombre()` y `actualizar_tarifa_base()`
controlan modificaciones. Las fechas de una reserva no se reemplazan: para cambiar una estancia
se cancela la reserva y se crea otra, de manera que se compruebe nuevamente la disponibilidad.

## 4. Sobreescritura y polimorfismo

Las tres hijas sobrescriben los dos métodos de `Habitacion`. La individual puede añadir $15.000
por desayuno; la doble, $20.000 por dos camas; la suite, $80.000 por jacuzzi. Son reglas propuestas
para la actividad, no tarifas obtenidas de un hotel real.

En `main()`, `habitaciones` contiene una instancia de cada especialización. Un único ciclo llama
`mostrar_informacion()` y `calcular_tarifa()` sobre cada objeto. No usa condicionales por tipo.
Los condicionales dentro de cada implementación evalúan datos propios, no seleccionan manualmente
qué clase debe atender la llamada. También se utiliza el mismo contrato al fijar la tarifa de una reserva.

## 5. Relaciones y composición

Cada `Reserva` conserva referencias al `Cliente` y a la `Habitacion` existentes. Ambos objetos pueden
participar en otras reservas y existen independientemente de ellas. Estas dos relaciones son asociaciones.
`Hotel` registra habitaciones y reservas, pero no crea las habitaciones.

La composición se aplica entre `Reserva` y `DetalleEstadia`. El constructor de la reserva crea el detalle
a partir de las fechas; no recibe uno creado fuera ni permite sustituirlo mediante la interfaz pública.
Cada reserva tiene un detalle distinto, cuya función es describir esa estancia. No se resolvió mediante
herencia porque una reserva contiene una estancia, no es una estancia.

El ciclo de vida expresa pertenencia en el modelo. Python administra la memoria por referencias:
si alguien conserva una referencia al detalle, este puede seguir en memoria después de eliminar una
referencia a la reserva. No se pretende demostrar una destrucción física inmediata de objetos.

## 6. Fechas, precio y cancelaciones

Las fechas se reciben como objetos `date`. El intervalo incluye la entrada y excluye la salida.
Dos intervalos se cruzan cuando la entrada de cada uno es anterior a la salida del otro.
Esto contempla cruces parciales, intervalos contenidos y fechas idénticas, y permite estancias consecutivas.

El total es el número de noches multiplicado por la tarifa acordada al reservar. Conservar esa tarifa
evita que una actualización posterior de precios altere reservas existentes. Los ejemplos utilizan
valores enteros en COP; para una aplicación con impuestos y redondeos financieros se debería
definir otra política monetaria antes de ampliarla.

Cancelar cambia el estado, mantiene el registro y libera fechas. Una cancelación repetida conserva el
mismo estado. Los códigos no se reutilizan, incluso después de cancelar. El total mostrado en una
reserva cancelada es el valor originalmente acordado, no un cobro ni una penalización.

## 7. Excepciones y continuidad

| Excepción | Dónde se lanza | Situación |
|---|---|---|
| `FechasInvalidasError` | Constructor de `DetalleEstadia` | Fechas incompatibles, salida igual o anterior a la entrada, o tipos incorrectos. |
| `HabitacionOcupadaError` | `Hotel.crear_reserva()` | Otra reserva activa ocupa esa habitación en fechas que se cruzan. |
| `ReservaNoEncontradaError` | `Hotel.consultar_reserva()` | El código solicitado no existe; también se usa al cancelar. |

El programa principal provoca y captura cada excepción por separado y muestra un mensaje de
continuidad después de cada captura. Finalmente cancela una reserva y crea otra correctamente.
Una operación rechazada no se incorpora al registro. Las validaciones generales, como una tarifa
negativa, un identificador vacío o un código duplicado, usan `ValueError`.

## 8. Ajustes durante la preparación y verificación

La propuesta inicial planteaba seis clases concretas. Durante la implementación se añadió `Hotel`
para centralizar los registros y la comprobación de cruces, evitando cargar esa responsabilidad en
`main()` o en una reserva individual. También se fijó la tarifa al crear la reserva para evitar que
los cambios posteriores de la habitación alterasen su total.

Se integró la consulta `consultar_habitaciones_disponibles()` enviada por Juan José en el pull
request #1. Al revisarla se identificó que `se_cruza_con()` recibía una tupla, aunque esperaba
un objeto con fechas de entrada y salida. La corrección construye un `DetalleEstadia` para el
periodo consultado, reutilizando tanto su validación de fechas como la comparación existente.

También se añadió `listar_reservas_activas()` en el cambio solicitado por Jesús, preparado con
apoyo de Codex. Este método devuelve una tupla con las reservas cuyo estado es activo y conserva
las canceladas en el historial. Las dos consultas se muestran ahora en el programa principal y
figuran en el UML.

Se ejecutó `python main.py` y se comprobó la creación de reservas, el rechazo de fechas
inválidas y cruces, la consulta de una reserva inexistente, la cancelación y las dos nuevas consultas. El programa mostró
los mensajes correspondientes y continuó hasta finalizar la demostración. El equipo debe revisar
el funcionamiento y su correspondencia con el UML antes de la entrega.

## 9. Herramientas y uso de inteligencia artificial

Se utilizó OpenAI Codex como apoyo para interpretar los requisitos y desarrollar el diseño,
el código y la documentación del proyecto.

La propuesta generada se ajustó añadiendo la clase `Hotel`, precisando la composición y conservando
el precio acordado. La consulta de reservas activas y la corrección de la consulta de disponibilidad
también se prepararon con ese apoyo. El historial conserva el aporte enviado desde la cuenta
de Juan José y el cambio publicado desde la cuenta de Jesús.

Referencias: documento de la Actividad Colaborativa N.º 3 suministrado por la asignatura y requisitos
compartidos por el usuario. Se emplean módulos de la biblioteca estándar de Python: `abc`,
`datetime`, `math`, `unittest`, `contextlib` e `io`.

## 10. Conclusiones

La implementación permite relacionar los conceptos de orientación a objetos con un problema
delimitado de reservas. La separación de responsabilidades permite cambiar las tarifas por tipo
sin modificar el ciclo que recorre las habitaciones. El control de cruces exige definir con precisión
si la fecha de salida ocupa una noche; esa regla se refleja en el código.

La integración de la consulta de disponibilidad permitió identificar una dificultad concreta:
los métodos que comparan periodos deben recibir objetos con una estructura compatible. Reutilizar
`DetalleEstadia` resolvió esa diferencia y evitó duplicar la validación de fechas. La consulta de
reservas activas muestra cómo obtener una vista del registro sin borrar información del historial.

La versión integrada y su historial de cambios se encuentran en
https://github.com/JesUsDavIdd/sistema-reservas-hotel.
