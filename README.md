# Sistema de reservas de hotel

Proyecto propuesto para la Actividad Colaborativa N.º 3: Proyecto Final.

Repositorio público: [sistema-reservas-hotel](https://github.com/JesUsDavIdd/sistema-reservas-hotel).

## Integrantes

- Juan Jose Lopera Morales
- Jesus David Becerra Tascon

## Descripción

El sistema registra habitaciones y reservas de un hotel pequeño. Permite consultar una reserva,
cancelarla y calcular su valor según las noches y el tipo de habitación. Evita que dos reservas
activas ocupen la misma habitación en fechas que se cruzan.

El alcance es una demostración por consola, con información en memoria. No tiene menú interactivo,
base de datos, pagos ni conexión con hoteles reales. Al cerrar el programa se pierden los registros.
Los nombres y documentos del ejemplo son ficticios. Los valores se expresan en pesos colombianos.

## Archivos

```text
proyecto-hotel/
├── main.py                 # Casos normales y excepcionales
├── habitaciones.py        # Clase abstracta y tres especializaciones
├── clientes.py            # Datos del cliente
├── reservas.py            # Reserva y su detalle de estancia
├── hotel.py               # Registro y control de reservas
├── excepciones.py         # Tres excepciones del dominio
├── test_hotel.py           # Pruebas automatizadas
├── README.md
├── UML.md                  # Diagrama Mermaid y explicación
├── UML.svg                 # Diagrama que puede abrirse en un navegador
├── DECISIONES_DISENO.md
├── GUIA_EQUIPO.md           # Revisión y distribución de trabajo sugerida
└── .gitignore
```

## Ejecución

Requiere Python 3.10 o superior. No necesita instalar paquetes adicionales.
Abra una terminal dentro de la carpeta del proyecto y ejecute:

```bash
python main.py
```

En Windows también puede usar `py main.py` si ese es el comando de su instalación.
El programa muestra tres habitaciones, crea tres reservas, captura los tres errores personalizados,
cancela una reserva y crea otra en las fechas liberadas. Termina con `Demostración finalizada.`
No es necesario ingresar datos por teclado.

Para ejecutar las pruebas:

```bash
python -m unittest -v
```

## Reglas del ejemplo

- La estancia incluye la fecha de entrada y excluye la de salida. Una habitación puede recibir
  otra reserva el mismo día en que sale el cliente anterior.
- La salida debe ser posterior a la entrada. Se reciben objetos `datetime.date`, no cadenas ni horas.
- Individual: tarifa base más $15.000 por noche si incluye desayuno.
- Doble: tarifa base más $20.000 por noche si tiene dos camas.
- Suite: tarifa base más $80.000 por noche si tiene jacuzzi.
- El precio por noche queda fijado al crear la reserva.
- La cancelación conserva la reserva en el historial, pero libera las fechas. Repetirla no produce cambios.
- Los números de habitación y códigos de reserva son únicos. Un código cancelado no se reutiliza.
- Se permiten fechas pasadas para facilitar los ejemplos; no se controla la fecha actual.

## Programación orientada a objetos

`Habitacion` es abstracta porque no representa una opción reservable concreta y obliga a implementar
`calcular_tarifa()` y `mostrar_informacion()`. `Individual`, `Doble` y `Suite` heredan sus datos comunes
y sobrescriben esos dos métodos usando desayuno, camas y jacuzzi, respectivamente.

En `main.py`, una sola lista contiene los tres tipos. Un único ciclo invoca los dos métodos sin
preguntar por el tipo de objeto: esa es la demostración de polimorfismo.

Los atributos se almacenan con prefijo `_`, una convención de uso interno en Python. Las propiedades
permiten leerlos y los métodos de actualización validan los cambios. Este mecanismo no impide que
alguien acceda deliberadamente a un atributo interno.

`Reserva` se asocia con `Cliente` y `Habitacion`. Además construye su propio `DetalleEstadia`, que
forma parte de su estructura y no se comparte entre reservas: esta es la composición. No corresponde
usar herencia porque una reserva no es un detalle de estancia.

Se lanzan y capturan `HabitacionOcupadaError`, `FechasInvalidasError` y `ReservaNoEncontradaError`.
Después de cada captura el programa continúa. Las validaciones simples usan `ValueError`.

## Documentación y revisión

Consulte [el UML](UML.md), [el diagrama SVG](UML.svg),
[las decisiones de diseño](DECISIONES_DISENO.md) y la [guía del equipo](GUIA_EQUIPO.md).

Se utilizó OpenAI Codex como apoyo para organizar el paso a paso del proyecto y elaborar
el código, la documentación y las pruebas.
