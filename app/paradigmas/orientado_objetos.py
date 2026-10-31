"""Demostración académica de clases, herencia y encapsulamiento."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal

class ReglaNegocio(ABC):
    """Clase base abstracta: define el contrato de una regla de negocio."""
    @abstractmethod
    def validar_cantidad(self, cantidad: int) -> None:
        raise NotImplementedError


class PersonaCafe(ABC):
    def __init__(self, nombre: str):
        self._nombre = nombre.strip()

    @property
    def nombre(self) -> str:
        return self._nombre

    @abstractmethod
    def tipo(self) -> str:
        raise NotImplementedError


class ClienteCafe(PersonaCafe):
    def tipo(self) -> str:
        return "cliente"


class EmpleadoCafe(PersonaCafe):
    def tipo(self) -> str:
        return "empleado"


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
