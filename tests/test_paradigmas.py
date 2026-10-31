import unittest
from types import SimpleNamespace

from app.paradigmas.declarativo import categorias_activas
from app.paradigmas.funcional import calcular_totales, sumar_hasta
from app.paradigmas.imperativo import evaluar_ventas_diarias
from app.paradigmas.logico import puede_venderse
from app.paradigmas.orientado_objetos import ClienteCafe, EmpleadoCafe, PoliticaPedido


class ParadigmasTest(unittest.TestCase):
    def test_imperativo_procesa_ventas(self):
        resultado = evaluar_ventas_diarias([10, -2, 20], 25)
        self.assertEqual(resultado["cantidad"], 2)
        self.assertEqual(resultado["total"], 30)
        self.assertEqual(resultado["estado"], "meta alcanzada")

    def test_funcional_calcula_sin_mutar(self):
        self.assertEqual(
            calcular_totales(100, 10, 0.15),
            {
                "subtotal": 100,
                "descuento": 10,
                "impuesto": 13.5,
                "total": 103.5,
            },
        )
        self.assertEqual(sumar_hasta(4), 10)

    def test_logico_infiere_hechos(self):
        producto = SimpleNamespace(estado="1", nombre="Café")
        self.assertTrue(puede_venderse(producto, 1, True))
        self.assertFalse(puede_venderse(producto, 1, False))

    def test_poo_encapsula_y_hereda(self):
        self.assertEqual(ClienteCafe(" Ana ").nombre, "Ana")
        self.assertEqual(ClienteCafe("Ana").tipo(), "cliente")
        self.assertEqual(EmpleadoCafe("Luis").tipo(), "empleado")
        PoliticaPedido().validar_cantidad(1)

    def test_declarativo_expone_consulta(self):
        self.assertTrue(callable(categorias_activas))


if __name__ == "__main__":
    unittest.main()
