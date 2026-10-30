"""Paradigma orientado a objetos: herencia y encapsulación de reglas de negocio."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal

class ReglaNegocio(ABC):
    """Clase base abstracta: define el contrato de una regla de negocio."""
    @abstractmethod
    def validar_cantidad(self, cantidad: int) -> None:
        raise NotImplementedError

@dataclass(frozen=True)
class PoliticaPedido(ReglaNegocio):
    """Implementación concreta que hereda el contrato de ReglaNegocio."""
    descuento_maximo: Decimal = Decimal("100000.00")

    def validar_descuento(self, descuento: Decimal, subtotal: Decimal) -> None:
        if descuento < 0:
            raise ValueError("El descuento no puede ser negativo.")
        if descuento > subtotal:
            raise ValueError("El descuento no puede superar el subtotal.")
        if descuento > self.descuento_maximo:
            raise ValueError("El descuento supera el límite permitido.")

    def validar_cantidad(self, cantidad: int) -> None:
        if cantidad < 1:
            raise ValueError("La cantidad de cada producto debe ser al menos 1.")
