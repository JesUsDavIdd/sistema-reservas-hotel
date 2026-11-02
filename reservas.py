"""Reservas y detalles de la estancia que pertenece a cada reserva."""

from datetime import date, datetime
from excepciones import FechasInvalidasError


class DetalleEstadia:
    def __init__(self, entrada, salida):
        # Se usan días completos. La fecha de salida no cuenta como noche ocupada.
        if (not isinstance(entrada, date) or isinstance(entrada, datetime)
                or not isinstance(salida, date) or isinstance(salida, datetime)
                or salida <= entrada):
            raise FechasInvalidasError("La salida debe ser posterior a la entrada; use fechas date.")
        self._entrada = entrada
        self._salida = salida

    @property
    def entrada(self):
        return self._entrada

    @property
    def salida(self):
        return self._salida

    def calcular_noches(self):
        return (self.salida - self.entrada).days

    def se_cruza_con(self, otro):
        return self.entrada < otro.salida and otro.entrada < self.salida


class Reserva:
    def __init__(self, codigo, cliente, habitacion, entrada, salida):
        if not isinstance(codigo, str) or not codigo.strip():
            raise ValueError("El código de reserva es obligatorio.")
        self._codigo = codigo.strip()
        self._cliente = cliente
        self._habitacion = habitacion
        # Composición: cada reserva construye su detalle y no permite reemplazarlo.
        self._detalle = DetalleEstadia(entrada, salida)
        self._activa = True
        # Se conserva la tarifa pactada aunque luego cambie la del hotel.
        self._tarifa_acordada = habitacion.calcular_tarifa()

    @property
    def codigo(self):
        return self._codigo

    @property
    def cliente(self):
        return self._cliente

    @property
    def habitacion(self):
        return self._habitacion

    @property
    def detalle(self):
        return self._detalle

    @property
    def activa(self):
        return self._activa

    @property
    def tarifa_acordada(self):
        return self._tarifa_acordada

    def calcular_total(self):
        return self.detalle.calcular_noches() * self.tarifa_acordada

    def cancelar(self):
        self._activa = False

    def mostrar_informacion(self):
        estado = "activa" if self.activa else "cancelada"
        noches = self.detalle.calcular_noches()
        unidad = "noche" if noches == 1 else "noches"
        return (f"{self.codigo} | {self.cliente.nombre} | Habitación {self.habitacion.numero} | "
                f"{self.detalle.entrada} a {self.detalle.salida} | "
                f"{noches} {unidad} | Total: ${self.calcular_total():,.0f} COP | {estado}")
