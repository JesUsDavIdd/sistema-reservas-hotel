"""Pruebas de funcionamiento. Ejecutar: python -m unittest -v."""

from contextlib import redirect_stdout
from datetime import date, datetime
from io import StringIO
import unittest

from clientes import Cliente
from excepciones import FechasInvalidasError, HabitacionOcupadaError, ReservaNoEncontradaError
from habitaciones import Habitacion, Individual, Doble, Suite
from hotel import Hotel
from main import main
from reservas import DetalleEstadia


class PruebasHabitaciones(unittest.TestCase):
    def test_no_se_puede_crear_habitacion_abstracta(self):
        with self.assertRaises(TypeError):
            Habitacion("101", 100000)

    def test_tarifas_segun_datos_de_cada_tipo(self):
        casos = [(Individual("101", 100000, True), 115000),
                 (Individual("102", 100000, False), 100000),
                 (Doble("201", 160000, 2), 180000),
                 (Doble("202", 160000, 1), 160000),
                 (Suite("301", 250000, True), 330000),
                 (Suite("302", 250000, False), 250000)]
        for habitacion, esperado in casos:
            with self.subTest(numero=habitacion.numero):
                self.assertEqual(habitacion.calcular_tarifa(), esperado)

    def test_informacion_especifica(self):
        self.assertIn("Desayuno: sí", Individual("101", 100000, True).mostrar_informacion())
        self.assertIn("Camas: 2", Doble("201", 160000, 2).mostrar_informacion())
        self.assertIn("Jacuzzi: sí", Suite("301", 250000, True).mostrar_informacion())

    def test_tarifas_invalidas_y_valor_anterior_conservado(self):
        habitacion = Individual("101", 100000, False)
        for valor in (0, -1, True, "100", float("nan"), float("inf")):
            with self.subTest(valor=valor):
                with self.assertRaises(ValueError):
                    habitacion.actualizar_tarifa_base(valor)
                self.assertEqual(habitacion.tarifa_base, 100000)

    def test_tarifa_se_actualiza_mediante_metodo(self):
        habitacion = Individual("101", 100000, True)
        habitacion.actualizar_tarifa_base(120000)
        self.assertEqual(habitacion.calcular_tarifa(), 135000)
        with self.assertRaises(AttributeError):
            habitacion.tarifa_base = -1

    def test_atributos_propios_validan_entrada(self):
        for fabrica in (lambda: Individual("101", 100000, "sí"),
                        lambda: Doble("201", 160000, 3),
                        lambda: Doble("201", 160000, True),
                        lambda: Suite("301", 250000, 1),
                        lambda: Individual(" ", 100000, True)):
            with self.assertRaises(ValueError):
                fabrica()


class PruebasReservas(unittest.TestCase):
    def setUp(self):
        self.hotel = Hotel("Los Cedros")
        self.habitacion = Individual("101", 100000, True)
        self.hotel.agregar_habitacion(self.habitacion)
        self.hotel.agregar_habitacion(Doble("201", 160000, 2))
        self.cliente = Cliente("1001", "Ana Ruiz")
        self.entrada = date(2026, 12, 1)
        self.salida = date(2026, 12, 4)

    def crear(self, codigo="R1", numero="101", entrada=None, salida=None):
        return self.hotel.crear_reserva(codigo, self.cliente, numero,
                                       entrada or self.entrada, salida or self.salida)

    def test_reserva_guarda_relaciones_con_objetos_originales(self):
        reserva = self.crear()
        self.assertIs(reserva.cliente, self.cliente)
        self.assertIs(reserva.habitacion, self.habitacion)
        self.assertIs(self.hotel.consultar_reserva("R1"), reserva)

    def test_tres_noches_y_total(self):
        reserva = self.crear()
        self.assertEqual(reserva.detalle.calcular_noches(), 3)
        self.assertEqual(reserva.calcular_total(), 345000)

    def test_cada_reserva_tiene_su_propio_detalle(self):
        primera = self.crear()
        segunda = self.crear("R2", "201")
        self.assertIsNot(primera.detalle, segunda.detalle)
        with self.assertRaises(AttributeError):
            primera.detalle = segunda.detalle

    def test_noches_cambio_de_mes_y_anio_bisiesto(self):
        detalle = DetalleEstadia(date(2028, 2, 28), date(2028, 3, 1))
        self.assertEqual(detalle.calcular_noches(), 2)

    def test_fechas_invalidas_no_guardan_reserva(self):
        for entrada, salida in ((self.salida, self.entrada), (self.entrada, self.entrada),
                                ("2026-12-01", self.salida),
                                (datetime(2026, 12, 1), self.salida)):
            with self.subTest(entrada=entrada, salida=salida):
                with self.assertRaises(FechasInvalidasError):
                    self.hotel.crear_reserva("R1", self.cliente, "101", entrada, salida)
                self.assertEqual(len(self.hotel.listar_reservas()), 0)

    def test_cruces_rechazados_y_reserva_original_conservada(self):
        original = self.crear()
        casos = [(date(2026, 12, 2), date(2026, 12, 3)),
                 (date(2026, 11, 30), date(2026, 12, 5)),
                 (date(2026, 11, 30), date(2026, 12, 2)),
                 (date(2026, 12, 3), date(2026, 12, 5)),
                 (self.entrada, self.salida)]
        for entrada, salida in casos:
            with self.subTest(entrada=entrada, salida=salida):
                with self.assertRaises(HabitacionOcupadaError):
                    self.crear("R2", entrada=entrada, salida=salida)
                self.assertEqual(self.hotel.listar_reservas(), (original,))

    def test_salida_y_entrada_mismo_dia_no_se_cruzan(self):
        self.crear()
        self.crear("R2", entrada=self.salida, salida=date(2026, 12, 5))
        self.crear("R3", entrada=date(2026, 11, 30), salida=self.entrada)
        self.assertEqual(len(self.hotel.listar_reservas()), 3)

    def test_dos_habitaciones_pueden_reservarse_mismas_fechas(self):
        self.crear()
        self.crear("R2", "201")
        self.assertEqual(len(self.hotel.listar_reservas()), 2)

    def test_cancelar_libera_fechas_y_conserva_historial(self):
        original = self.crear()
        self.hotel.cancelar_reserva("R1")
        nueva = self.crear("R2")
        self.assertFalse(original.activa)
        self.assertTrue(nueva.activa)
        self.assertEqual(len(self.hotel.listar_reservas()), 2)

    def test_consulta_y_cancelacion_inexistentes(self):
        for operacion in (self.hotel.consultar_reserva, self.hotel.cancelar_reserva):
            with self.assertRaises(ReservaNoEncontradaError):
                operacion("R99")
        self.assertTrue(self.crear().activa)

    def test_codigo_duplicado_no_reemplaza_reserva(self):
        original = self.crear()
        with self.assertRaises(ValueError):
            self.crear(" R1 ", "201")
        self.assertIs(self.hotel.consultar_reserva("R1"), original)

    def test_habitacion_no_registrada(self):
        with self.assertRaises(ValueError):
            self.crear(numero="999")
        self.assertEqual(self.hotel.listar_reservas(), ())

    def test_numero_habitacion_duplicado(self):
        with self.assertRaises(ValueError):
            self.hotel.agregar_habitacion(Suite("101", 250000, True))
        self.assertIs(self.hotel.listar_habitaciones()[0], self.habitacion)

    def test_cambio_de_tarifa_no_altera_precio_pactado(self):
        anterior = self.crear()
        self.habitacion.actualizar_tarifa_base(200000)
        nueva = self.crear("R2", entrada=self.salida, salida=date(2026, 12, 5))
        self.assertEqual(anterior.calcular_total(), 345000)
        self.assertEqual(nueva.calcular_total(), 215000)

    def test_listado_no_expone_diccionario_interno(self):
        self.crear()
        listado = list(self.hotel.listar_reservas())
        listado.clear()
        self.assertEqual(len(self.hotel.listar_reservas()), 1)

    def test_cliente_valida_cambios(self):
        with self.assertRaises(ValueError):
            self.cliente.actualizar_nombre(" ")
        self.assertEqual(self.cliente.nombre, "Ana Ruiz")
        self.cliente.actualizar_nombre(" Ana María ")
        self.assertEqual(self.cliente.nombre, "Ana María")

    def test_main_captura_excepciones_y_termina(self):
        salida = StringIO()
        with redirect_stdout(salida):
            main()
        texto = salida.getvalue()
        self.assertIn("está ocupada", texto)
        self.assertIn("La salida debe ser posterior", texto)
        self.assertIn("No existe la reserva R99", texto)
        self.assertEqual(texto.count("El sistema continúa"), 3)
        self.assertIn("R6 | Carlos Gil", texto)
        self.assertIn("Demostración finalizada.", texto)


if __name__ == "__main__":
    unittest.main()
