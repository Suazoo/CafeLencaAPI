
## Clientes

`GET /clientes/` devuelve:

```json
[
  {
    "idCliente": 1,
    "Persona_idPersona": 1,
    "persona": {
      "idPersona": 1,
      "Pnombre": "Ana",
      "Snombre": null,
      "Papellido": "López",
      "Sapellido": null,
      "correo": "ana@example.com",
      "Fecha_registro": "2026-10-28T12:00:00"
    }
  }
]
```

`POST /clientes/` recibe `Pnombre`, `Papellido`, `correo` obligatorios; `Snombre`, `Sapellido` y `telefono` son opcionales. `PUT /clientes/{id}` actualiza los campos enviados. El correo debe ser único.

## Catálogo

- `GET /categorias/`
- `POST /categorias/`: `{ "nombre": "Bebidas", "descripcion": "Cafés y bebidas" }`
- `GET /productos/`
- `GET /productos/disponibles`
- `POST /productos/`: `{ "nombre": "Latte", "precio": "65.00", "Categoria_idCategoria": 1, "descripcion": "Café con leche" }`
- `PATCH /productos/{id}` acepta los campos que se quieran cambiar.

## Pedido y factura

`POST /pedidos/` recibe los identificadores opcionales de cliente/mesa/método de pago/empleado, un descuento y al menos un detalle. Los productos deben existir y estar activos. El backend calcula importes; el frontend no debe confiar en totales calculados en el navegador.

```json
{
  "Cliente_idCliente": 1,
  "Mesa_idMesa": 2,
  "MetodoPago_idMetodoPago": 1,
  "Empleado_idEmpleado": 1,
  "descuento": "0.00",
  "detalles": [
    { "Producto_idProducto": 1, "cantidad": 2 }
  ]
}
```

La respuesta incluye `detalles`, `factura` y `alertas_inventario`. La creación del pedido, detalles y factura se confirma como una sola transacción. La tasa se configura con `TAX_RATE`. Para descargar el PDF, abre `GET /pedidos/{id}/factura/pdf` como descarga de archivo.

## Catálogos auxiliares y otras pantallas

- Mesas activas: `GET /catalogos/mesas`
- Métodos de pago: `GET /catalogos/metodos-pago`
- Empleados: `GET /catalogos/empleados`
- Reservas: `GET /reservas/`, `POST /reservas/`
- Resumen: `GET /dashboard/resumen`
- Ventas: `GET /reportes/ventas?desde=2026-10-01&hasta=2026-10-31`
- Recomendaciones: `GET /motor-logico/recomendaciones`
- Existencias: `GET /inventario/`, actualización de stock `PATCH /inventario/{id}` con body `{ "cantidad_actual": 12.500 }`

## Manejo de errores

La API responde con códigos HTTP habituales:
- `201`: recurso creado.
- `404`: identificador no encontrado.
- `409`: conflicto de unicidad/integridad.
- `422`: datos inválidos o regla de negocio incumplida.
- `500`: error inesperado del servidor; revisar la terminal del backend sin compartir credenciales.

Las respuestas de error de FastAPI contienen un campo `detail`. Muestra ese mensaje de forma amigable en la interfaz.
