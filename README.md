# Café Lenca — Backend

API de gestión de cafetería desarrollada con FastAPI, SQLAlchemy 2, Pydantic y PostgreSQL/Supabase.

## 1. Requisitos

- Python 3.11 o superior recomendado.
- Una base de datos PostgreSQL de Café Lenca con las tablas existentes del proyecto.
- Credenciales de Supabase.

## 2. Configurar entorno

En PowerShell, desde la carpeta `cafe-paradigmas`:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```
## 3. Iniciar API

```powershell
uvicorn app.main:app --reload
```

- Swagger/OpenAPI: http://127.0.0.1:8000/docs
- Raíz: http://127.0.0.1:8000/
- Estado de API: http://127.0.0.1:8000/health
- Estado de base de datos: http://127.0.0.1:8000/health/db

## 4. Endpoints preparados para el frontend

| Método | Ruta | Uso |
|---|---|---|
| GET, POST | `/clientes/` | Listar y registrar clientes |
| GET, PUT, DELETE | `/clientes/{id}` | Consultar, actualizar y eliminar clientes |
| GET, POST | `/categorias/` | Listar y registrar categorías |
| GET | `/productos/` | Listar catálogo |
| GET | `/productos/disponibles` | Listar productos activos |
| GET, POST, PATCH | `/productos/{id}` / `/productos/` | Consultar, crear y actualizar productos |
| GET | `/catalogos/mesas` | Mesas activas |
| GET | `/catalogos/metodos-pago` | Métodos de pago activos |
| GET | `/catalogos/empleados` | Empleados |
| GET, POST | `/pedidos/` | Consultar y registrar pedidos |
| GET | `/pedidos/{id}` | Consultar pedido con detalles y factura |
| GET | `/pedidos/{id}/factura/pdf` | Descargar la factura en PDF |
| PATCH | `/pedidos/{id}/estado` | Actualizar estado |
| GET, POST | `/reservas/` | Consultar y crear reservas |
| GET | `/dashboard/resumen` | Contadores y facturación agregada |
| GET | `/reportes/ventas` | Reporte de facturación, opcionalmente por fechas |
| GET | `/motor-logico/recomendaciones` | Recomendaciones de productos activos |
| GET | `/motor-logico/reglas` | Reglas que aplica el motor lógico |
| GET, PATCH | `/inventario/` y `/inventario/{id}` | Consultar existencias y actualizar stock |

### Ejemplo de creación de pedido

```json
{
  "Cliente_idCliente": 1,
  "Mesa_idMesa": 1,
  "MetodoPago_idMetodoPago": 1,
  "Empleado_idEmpleado": 1,
  "descuento": "0.00",
  "detalles": [
    {"Producto_idProducto": 1, "cantidad": 2},
    {"Producto_idProducto": 2, "cantidad": 1}
  ]
}
```
## 5. Los cinco paradigmas

Los ejemplos académicos están separados en `app/paradigmas/`:

- `imperativo.py`: secuencia de pasos del proceso de pedido.
- `orientado_objetos.py`: clase abstracta `ReglaNegocio`, herencia y política de pedido encapsulada.
- `funcional.py`: funciones puras para normalización y cálculos monetarios, usadas por pedidos/clientes.
- `logico.py`: reglas declarativas de venta, conectadas con `app/motor_logico/reglas.py`.
- `declarativo.py`: consultas ORM que describen los datos deseados; los modelos están en `app/models/`.

`app/motor_logico/` contiene reglas ejecutables reales de disponibilidad, cantidades, inventario y recomendaciones.


