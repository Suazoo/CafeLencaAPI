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

Antes de crear pedidos, ejecuta `sql/schema.sql` y después `sql/functions.sql` en el
SQL Editor de Supabase. La función `public.registrar_pedido(jsonb)` es la operación
transaccional usada por la API para crear pedido, detalles, factura y descuento de
inventario. No contiene credenciales y puede revisarse como parte del código fuente.

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
| POST | `/motor-logico/ia` | Interpretar una solicitud del cliente con Gemini usando el catálogo validado |
| POST | `/motor-logico/ia/pedido` | Convertir una solicitud en una propuesta de pedido |
| POST | `/motor-logico/ia/resumen-ventas` | Explicar un reporte de ventas |
| POST | `/motor-logico/ia/alertas-inventario` | Priorizar alertas de inventario |
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
Si un producto tiene receta en `ingrediente_has_producto`, el motor lógico valida y descuenta el inventario relacionado. Los productos sin receta registrada no bloquean el pedido por inventario.

## 5. Integración de inteligencia artificial

El proyecto utiliza Gemini como complemento del motor lógico. La IA no decide qué productos
pueden venderse: primero `recomendar_productos` selecciona productos activos del catálogo y
después Gemini interpreta la solicitud escrita por el cliente para ordenar las opciones y
explicar por qué pueden ser adecuadas.

El flujo es:

```text
Solicitud del cliente
        ↓
Motor lógico valida el catálogo
        ↓
Gemini interpreta preferencias y contexto
        ↓
Respuesta con mensaje, productos válidos y motivos
```

### Configuración

La clave debe configurarse únicamente como variable de entorno en el backend o en Render:

```text
GEMINI_API_KEY=tu_clave
GEMINI_MODEL=gemini-3.5-flash-lite
```

### Endpoint de IA

`POST /motor-logico/ia`

Solicitud:

```json
{
  "solicitud": "Quiero algo dulce y barato para acompañar el café",
  "limite": 3
}
```

Respuesta:

```json
{
  "mensaje": "Te recomiendo estas opciones dulces y económicas.",
  "productos": [
    {
      "idProducto": 9,
      "nombre": "Pan de coco",
      "precio": 25.0,
      "motivo": "Es dulce y económico."
    }
  ],
  "motor_principal": true,
  "ia": "gemini-3.5-flash-lite"
}
```

El backend filtra la respuesta de Gemini contra el catálogo validado para evitar que la IA
invente productos o precios. Si Gemini no está disponible, el frontend conserva las
recomendaciones normales del motor lógico.

### Cómo se usa en el frontend

En la pantalla **Motor lógico**, escribe una solicitud como:

- `Quiero algo caliente y no tan caro`.
- `Busco un postre dulce`.
- `Quiero una bebida fría`.
- `Necesito algo para acompañar el café`.

El frontend envía la solicitud mediante `POST /motor-logico/ia` y muestra las recomendaciones
en [MotorLogicoView.vue](../../Frontend/Cafe-Lenca/src/views/MotorLogicoView.vue).

## 6. Los cinco paradigmas

Los ejemplos académicos están separados en `app/paradigmas/` y no son necesarios para
levantar la API. Su objetivo es facilitar la lectura y defensa del proyecto:

- `imperativo.py`: variables, secuencia, ciclo y condicionales para evaluar ventas.
- `orientado_objetos.py`: clases, constructor, encapsulamiento, herencia y una política de pedido.
- `funcional.py`: funciones puras con `map`, `filter`, `reduce` y recursividad.
- `logico.py`: hechos, reglas e inferencia para decidir si un producto puede venderse.
- `declarativo.py`: consultas ORM con selección, filtros, agrupación y ordenamiento.

`app/motor_logico/` contiene reglas ejecutables reales de disponibilidad, cantidades,
inventario y recomendaciones. La carpeta `app/paradigmas/` es únicamente demostrativa.

## 7. Usos actuales y futuros de la IA

Las utilidades actualmente disponibles desde el frontend son:

- **Asistente para tomar pedidos:** `POST /motor-logico/ia/pedido` convierte frases
  naturales en productos y cantidades del catálogo validado.
- **Resumen de ventas:** `POST /motor-logico/ia/resumen-ventas` explica un reporte
  y devuelve puntos clave y una recomendación.
- **Alertas inteligentes de inventario:** `POST /motor-logico/ia/alertas-inventario`
  prioriza alertas recibidas y propone una acción.

Estas funciones no reemplazan las reglas de negocio: el backend valida el catálogo
antes de construir propuestas de pedidos y no permite usar productos inexistentes.

Otros usos que pueden agregarse en el futuro:

- **Asistente para tomar pedidos:** convertir frases naturales en productos y cantidades para
  preparar un pedido.
- **Resumen de ventas:** explicar tendencias del reporte diario o mensual en lenguaje sencillo.
- **Alertas inteligentes de inventario:** priorizar compras según consumo, stock mínimo y
  productos más vendidos.
- **Atención al cliente:** responder preguntas sobre productos, precios, horarios y reservas
  usando únicamente información del sistema.
- **Pronóstico de demanda:** estimar qué productos podrían venderse más en determinados días.
- **Clasificación de comentarios:** detectar satisfacción, quejas y oportunidades de mejora.

## 8. Pruebas

Ejecuta desde `cafe-paradigmas`:

```powershell
python -m unittest discover -s tests -v
```

Las pruebas no necesitan conectarse a Supabase; validan los ejemplos de paradigmas y
las reglas puras para evitar regresiones durante la refactorización.
