"""Tipos de habitación y sus tarifas por noche."""

from abc import ABC, abstractmethod
from math import isfinite


class Habitacion(ABC):
    def __init__(self, numero, tarifa_base):
        if not isinstance(numero, str) or not numero.strip():
            raise ValueError("El número de habitación es obligatorio.")
        self._numero = numero.strip()
        self.actualizar_tarifa_base(tarifa_base)

    @property
    def numero(self):
        return self._numero

    @property
    def tarifa_base(self):
        return self._tarifa_base

    def actualizar_tarifa_base(self, valor):
        if (isinstance(valor, bool) or not isinstance(valor, (int, float))
                or not isfinite(valor) or valor <= 0):
            raise ValueError("La tarifa debe ser un número positivo.")
        self._tarifa_base = valor

    @abstractmethod
    def calcular_tarifa(self):
        """Devuelve el valor por noche según el tipo de habitación."""
        pass

    @abstractmethod
    def mostrar_informacion(self):
        pass


class Individual(Habitacion):
    def __init__(self, numero, tarifa_base, incluye_desayuno):
        super().__init__(numero, tarifa_base)
        if not isinstance(incluye_desayuno, bool):
            raise ValueError("Debe indicar si incluye desayuno con True o False.")
        self._incluye_desayuno = incluye_desayuno

    @property
    def incluye_desayuno(self):
        return self._incluye_desayuno

    def calcular_tarifa(self):
        return self.tarifa_base + (15000 if self.incluye_desayuno else 0)

    def mostrar_informacion(self):
        desayuno = "sí" if self.incluye_desayuno else "no"
        return f"Individual {self.numero} | Desayuno: {desayuno}"


class Doble(Habitacion):
    def __init__(self, numero, tarifa_base, camas):
        super().__init__(numero, tarifa_base)
        if isinstance(camas, bool) or not isinstance(camas, int) or camas not in (1, 2):
            raise ValueError("La habitación doble debe tener una o dos camas.")
        self._camas = camas

    @property
    def camas(self):
        return self._camas

    def calcular_tarifa(self):
        return self.tarifa_base + (20000 if self.camas == 2 else 0)

    def mostrar_informacion(self):
        return f"Doble {self.numero} | Camas: {self.camas}"


class Suite(Habitacion):
    def __init__(self, numero, tarifa_base, tiene_jacuzzi):
        super().__init__(numero, tarifa_base)
        if not isinstance(tiene_jacuzzi, bool):
            raise ValueError("Debe indicar si tiene jacuzzi con True o False.")
        self._tiene_jacuzzi = tiene_jacuzzi

    @property
    def tiene_jacuzzi(self):
        return self._tiene_jacuzzi

    def calcular_tarifa(self):
        return self.tarifa_base + (80000 if self.tiene_jacuzzi else 0)

    def mostrar_informacion(self):
        jacuzzi = "sí" if self.tiene_jacuzzi else "no"
        return f"Suite {self.numero} | Jacuzzi: {jacuzzi}"
