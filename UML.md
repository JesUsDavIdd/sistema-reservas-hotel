# Diagrama de clases

El diagrama se muestra en GitHub mediante Mermaid. También está disponible como [SVG](UML.svg).
Se omiten las propiedades de lectura para facilitar la lectura; sus nombres corresponden a los
atributos internos sin el prefijo `_`.

```mermaid
classDiagram
    class Habitacion {
        <<abstract>>
        #str _numero
        #number _tarifa_base
        +actualizar_tarifa_base(valor)
        +calcular_tarifa()*
        +mostrar_informacion()*
    }
    class Individual {
        -bool _incluye_desayuno
        +calcular_tarifa()
        +mostrar_informacion()
    }
    class Doble {
        -int _camas
        +calcular_tarifa()
        +mostrar_informacion()
    }
    class Suite {
        -bool _tiene_jacuzzi
        +calcular_tarifa()
        +mostrar_informacion()
    }
    class Cliente {
        -str _documento
        -str _nombre
        +actualizar_nombre(nombre)
        +mostrar_informacion()
    }
    class DetalleEstadia {
        -date _entrada
        -date _salida
        +calcular_noches()
        +se_cruza_con(otro)
    }
    class Reserva {
        -str _codigo
        -Cliente _cliente
        -Habitacion _habitacion
        -DetalleEstadia _detalle
        -bool _activa
        -number _tarifa_acordada
        +calcular_total()
        +cancelar()
        +mostrar_informacion()
    }
    class Hotel {
        -str _nombre
        -dict _habitaciones
        -dict _reservas
        +agregar_habitacion(habitacion)
        +listar_habitaciones()
        +crear_reserva(codigo, cliente, numero, entrada, salida)
        +consultar_reserva(codigo)
        +cancelar_reserva(codigo)
        +listar_reservas()
        +listar_reservas_activas()
        +consultar_habitaciones_disponibles(entrada, salida)
    }
    class FechasInvalidasError {
        <<exception>>
    }
    class HabitacionOcupadaError {
        <<exception>>
    }
    class ReservaNoEncontradaError {
        <<exception>>
    }
    Habitacion <|-- Individual
    Habitacion <|-- Doble
    Habitacion <|-- Suite
    Cliente "1" <-- "0..*" Reserva : cliente
    Habitacion "1" <-- "0..*" Reserva : habitacion
    Reserva "1" *-- "1" DetalleEstadia : crea y contiene
    Hotel "0..*" --> "0..*" Habitacion : registra
    Hotel "1" --> "0..*" Reserva : registra
    Hotel ..> HabitacionOcupadaError : lanza
    Hotel ..> ReservaNoEncontradaError : lanza
    Hotel ..> DetalleEstadia : construye periodo de consulta
    DetalleEstadia ..> FechasInvalidasError : lanza
```

El rombo lleno indica composición; la flecha con triángulo indica herencia.
Cada reserva utiliza un cliente, una habitación y su propio detalle. Los intervalos de reservas
activas de una misma habitación no pueden cruzarse. El modelo no impide que la misma habitación
sea registrada en distintas instancias de `Hotel`; la demostración usa un único hotel.
Las tres excepciones heredan de `Exception` en el código; esa clase estándar se omite aquí.
