"""Demostración del sistema: ejecutar con python main.py."""

from datetime import date
from clientes import Cliente
from excepciones import FechasInvalidasError, HabitacionOcupadaError, ReservaNoEncontradaError
from habitaciones import Individual, Doble, Suite
from hotel import Hotel


def main():
    hotel = Hotel("Hotel Los Cedros")
    habitaciones = [Individual("101", 100000, True), Doble("201", 160000, 2), Suite("301", 250000, True)]
    clientes = [Cliente("1001", "Ana Ruiz"), Cliente("1002", "Carlos Gil"), Cliente("1003", "Laura Pérez")]

    print(f"RESERVAS - {hotel.nombre}")
    # Una colección heterogénea y un solo ciclo para llamar los dos métodos.
    for habitacion in habitaciones:
        hotel.agregar_habitacion(habitacion)
        print(habitacion.mostrar_informacion(), f"| Noche: ${habitacion.calcular_tarifa():,.0f} COP")

    print("\nReservas creadas:")
    r1 = hotel.crear_reserva("R1", clientes[0], "101", date(2026, 12, 1), date(2026, 12, 4))
    r2 = hotel.crear_reserva("R2", clientes[1], "201", date(2026, 12, 2), date(2026, 12, 4))
    r3 = hotel.crear_reserva("R3", clientes[2], "301", date(2026, 12, 1), date(2026, 12, 2))
    for reserva in (r1, r2, r3):
        print(reserva.mostrar_informacion())

    print("\nCasos excepcionales:")
    try:
        hotel.crear_reserva("R4", clientes[1], "101", date(2026, 12, 2), date(2026, 12, 5))
    except HabitacionOcupadaError as error:
        print(error)
    print("El sistema continúa después del intento de reserva duplicada.")

    try:
        hotel.crear_reserva("R5", clientes[0], "201", date(2026, 12, 8), date(2026, 12, 7))
    except FechasInvalidasError as error:
        print(error)
    print("El sistema continúa después de las fechas inválidas.")

    try:
        hotel.consultar_reserva("R99")
    except ReservaNoEncontradaError as error:
        print(error)
    print("El sistema continúa después de la consulta fallida.")

    print("\nCancelación y nueva reserva:")
    hotel.cancelar_reserva("R1")
    print(hotel.consultar_reserva("R1").mostrar_informacion())
    nueva = hotel.crear_reserva("R6", clientes[1], "101", date(2026, 12, 1), date(2026, 12, 4))
    print(nueva.mostrar_informacion())

    print("\nReservas activas:")
    for reserva in hotel.listar_reservas_activas():
        print(reserva.mostrar_informacion())

    print("\nHabitaciones disponibles del 2 al 3 de diciembre de 2026:")
    disponibles = hotel.consultar_habitaciones_disponibles(date(2026, 12, 2), date(2026, 12, 3))
    for habitacion in disponibles:
        print(habitacion.mostrar_informacion())
    if not disponibles:
        print("No hay habitaciones disponibles para esas fechas.")
    print("\nDemostración finalizada.")


if __name__ == "__main__":
    main()
