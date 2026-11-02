"""Información básica de los clientes."""


class Cliente:
    def __init__(self, documento, nombre):
        if not isinstance(documento, str) or not documento.strip():
            raise ValueError("El documento del cliente es obligatorio.")
        self._documento = documento.strip()
        self.actualizar_nombre(nombre)

    @property
    def documento(self):
        return self._documento

    @property
    def nombre(self):
        return self._nombre

    def actualizar_nombre(self, nombre):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre del cliente es obligatorio.")
        self._nombre = nombre.strip()

    def mostrar_informacion(self):
        return f"{self.documento} - {self.nombre}"
