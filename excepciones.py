"""Errores propios del sistema de reservas."""


class FechasInvalidasError(Exception):
    pass


class HabitacionOcupadaError(Exception):
    pass


class ReservaNoEncontradaError(Exception):
    pass
