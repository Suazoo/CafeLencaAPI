# Arquitectura de Café Lenca

## Capas del backend

```text
      Vue 3 
        |
        | HTTP/JSON + CORS
        v
app/routers/       Endpoints FastAPI, validación HTTP y códigos de respuesta
        |
        v
app/services/      Casos de uso y transacciones de negocio
        |
        +------> app/motor_logico/   Reglas de venta, inventario y recomendaciones
        |
        +------> app/paradigmas/     Ejemplos académicos conectados al caso real
        |
        v
app/models/        Mapeo declarativo SQLAlchemy de las tablas existentes
        |
        v
app/core/database.py  Sesiones y conexión PostgreSQL/Supabase
```

## Clases de dominio principales

- `Persona`: datos personales compartidos; se relaciona uno a uno con `Cliente` o `Empleado`.
- `Cliente`: representa al cliente y enlaza con pedidos, reservas y preferencias.
- `Empleado`, `Rol`, `Rol_has_Empleado`: personal y asignación de roles.
- `Categoria`, `Producto`: catálogo de la cafetería.
- `Ingrediente`, `Ingrediente_has_Producto`, `Inventario`: receta de productos y existencias.
- `Mesa`, `Reserva`: mesas y reservaciones.
- `Pedido`, `DetallePedido`, `Factura`: cabecera, líneas y comprobante de venta.
- `MetodoPago`, `Telefono`, `PreferenciaCliente`: catálogos e información complementaria.

Las claves y nombres de columnas están mapeados desde `sql/schema.sql`. No se crea el esquema automáticamente.

## Dónde se ve cada paradigma

1. **Imperativo — `app/paradigmas/imperativo.py`:** pasos explícitos del flujo de un pedido. El servicio ejecuta las etapas en ese orden dentro de una transacción.
2. **Orientado a objetos — `app/paradigmas/orientado_objetos.py`:** `PoliticaPedido` hereda de `ReglaNegocio`; encapsula validaciones de cantidades y descuentos. Se utiliza en `PedidoService`.
3. **Funcional — `app/paradigmas/funcional.py`:** `normalizar_texto`, `calcular_totales`, `importes_detalles` y `total_importes` son funciones sin efectos secundarios. También se muestran `map`, `filter`, `reduce`, `lambda` y recursividad en `sumar_hasta`, sin reemplazar los cálculos existentes de pedidos.
4. **Lógico — `app/paradigmas/logico.py` y `app/motor_logico/reglas.py`:** `hechos_producto` construye hechos, `inferir_venta` aplica reglas y `puede_venderse` devuelve la conclusión. Las reglas de receta, inventario y recomendaciones se ejecutan al procesar pedidos.
5. **Declarativo — `app/paradigmas/declarativo.py` y `app/models/`:** consultas ORM expresan qué registros se necesitan y los modelos declaran tablas, columnas y relaciones. Los listados de productos/categorías reutilizan las consultas del ejemplo.

## Flujo transaccional de un pedido

1. Validar los identificadores de cliente/mesa/método de pago/empleado enviados.
2. Verificar que los productos existan, estén activos y tengan cantidades válidas.
3. Calcular subtotal, descuento, impuesto y total con funciones puras.
4. Crear el pedido y sus detalles.
5. Si hay receta configurada, validar y descontar ingredientes del inventario.
6. Crear factura.
7. Confirmar todo con un único `commit`; ante un error se hace `rollback`.

