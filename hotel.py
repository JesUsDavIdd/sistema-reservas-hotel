"""Registro de habitaciones, consulta y control de reservas."""

from excepciones import HabitacionOcupadaError, ReservaNoEncontradaError
from reservas import Reserva, DetalleEstadia


class Hotel:
    def __init__(self, nombre):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre del hotel es obligatorio.")
        self._nombre = nombre.strip()
        self._habitaciones = {}
        self._reservas = {}

    @property
    def nombre(self):
        return self._nombre

    def agregar_habitacion(self, habitacion):
        if habitacion.numero in self._habitaciones:
            raise ValueError("Ya existe una habitación con ese número.")
        self._habitaciones[habitacion.numero] = habitacion

    def listar_habitaciones(self):
        return tuple(self._habitaciones.values())

    def crear_reserva(self, codigo, cliente, numero, entrada, salida):
        if not isinstance(codigo, str) or not codigo.strip():
            raise ValueError("El código de reserva es obligatorio.")
        codigo = codigo.strip()
        if codigo in self._reservas:
            raise ValueError("Ya existe una reserva con ese código.")
        if numero not in self._habitaciones:
            raise ValueError("La habitación no está registrada.")
        nueva = Reserva(codigo, cliente, self._habitaciones[numero], entrada, salida)
        for reserva in self._reservas.values():
            if (reserva.activa and reserva.habitacion.numero == numero
                    and reserva.detalle.se_cruza_con(nueva.detalle)):
                raise HabitacionOcupadaError(f"La habitación {numero} está ocupada en esas fechas.")
        self._reservas[codigo] = nueva
        return nueva

    def consultar_reserva(self, codigo):
        if codigo not in self._reservas:
            raise ReservaNoEncontradaError(f"No existe la reserva {codigo}.")
        return self._reservas[codigo]

    def cancelar_reserva(self, codigo):
        self.consultar_reserva(codigo).cancelar()

    def listar_reservas(self):
        return tuple(self._reservas.values())

    def listar_reservas_activas(self):
        activas = []
        for reserva in self._reservas.values():
            if reserva.activa:
                activas.append(reserva)
        return tuple(activas)

    def consultar_habitaciones_disponibles(self, entrada, salida):
        periodo = DetalleEstadia(entrada, salida)
        disponibles = []
        for habitacion in self._habitaciones.values():
            ocupada = False
            for reserva in self._reservas.values():
                if reserva.activa and reserva.habitacion.numero == habitacion.numero:
                    if reserva.detalle.se_cruza_con(periodo):
                        ocupada = True
                        break
            if not ocupada:
                disponibles.append(habitacion)
        return tuple(disponibles)
