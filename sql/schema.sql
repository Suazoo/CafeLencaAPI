-- 1. Módulo de Personas y Usuarios
CREATE TABLE Persona (
    idPersona SERIAL PRIMARY KEY,
    Pnombre VARCHAR(45) NOT NULL,
    Snombre VARCHAR(45),
    Papellido VARCHAR(45) NOT NULL,
    Sapellido VARCHAR(45),
    correo VARCHAR(100) UNIQUE NOT NULL,
    Fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Telefono (
    idTelefono SERIAL PRIMARY KEY,
    numero VARCHAR(45) NOT NULL,
    Persona_idPersona INT REFERENCES Persona(idPersona) ON DELETE CASCADE
);

CREATE TABLE Cliente (
    idCliente SERIAL PRIMARY KEY,
    Persona_idPersona INT UNIQUE REFERENCES Persona(idPersona) ON DELETE CASCADE
);

CREATE TABLE Empleado (
    idEmpleado SERIAL PRIMARY KEY,
    Persona_idPersona INT UNIQUE REFERENCES Persona(idPersona) ON DELETE CASCADE
);

CREATE TABLE Rol (
    idRol SERIAL PRIMARY KEY,
    nombre VARCHAR(45) NOT NULL,
    estado VARCHAR(1) DEFAULT '1'
);

CREATE TABLE Rol_has_Empleado (
    Rol_idRol INT REFERENCES Rol(idRol) ON DELETE CASCADE,
    Empleado_idEmpleado INT REFERENCES Empleado(idEmpleado) ON DELETE CASCADE,
    PRIMARY KEY (Rol_idRol, Empleado_idEmpleado)
);

CREATE TABLE PreferenciaCliente (
    idPreferencia SERIAL PRIMARY KEY,
    tipo_preferencia VARCHAR(45) NOT NULL,
    valor VARCHAR(100) NOT NULL,
    Cliente_idCliente INT REFERENCES Cliente(idCliente) ON DELETE CASCADE
);

-- 2. Módulo de Mesas y Reservas
CREATE TABLE Mesa (
    idMesa SERIAL PRIMARY KEY,
    numero INT UNIQUE NOT NULL,
    capacidad INT NOT NULL,
    estado VARCHAR(1) DEFAULT '1'
);

CREATE TABLE Reserva (
    idReserva SERIAL PRIMARY KEY,
    fecha_reserva TIMESTAMP NOT NULL,
    cantidad_persona INT NOT NULL,
    estado VARCHAR(1) DEFAULT '1',
    Cliente_idCliente INT REFERENCES Cliente(idCliente) ON DELETE CASCADE,
    Mesa_idMesa INT REFERENCES Mesa(idMesa) ON DELETE SET NULL
);

-- 3. Módulo de Operaciones, Pedidos y Facturación
CREATE TABLE MetodoPago (
    idMetodoPago SERIAL PRIMARY KEY,
    nombre VARCHAR(45) NOT NULL,
    estado VARCHAR(1) DEFAULT '1'
);

CREATE TABLE Pedido (
    idPedido SERIAL PRIMARY KEY,
    fecha_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(1) DEFAULT '1',
    Cliente_idCliente INT REFERENCES Cliente(idCliente) ON DELETE SET NULL,
    Mesa_idMesa INT REFERENCES Mesa(idMesa) ON DELETE SET NULL,
    MetodoPago_idMetodoPago INT REFERENCES MetodoPago(idMetodoPago) ON DELETE SET NULL,
    Empleado_idEmpleado INT REFERENCES Empleado(idEmpleado) ON DELETE SET NULL
);

-- 4. Módulo de Catálogo, Productos e Inventario
CREATE TABLE Categoria (
    idCategoria SERIAL PRIMARY KEY,
    nombre VARCHAR(45) NOT NULL,
    descripcion VARCHAR(225),
    estado VARCHAR(1) DEFAULT '1'
);

CREATE TABLE Producto (
    idProducto SERIAL PRIMARY KEY,
    nombre VARCHAR(45) NOT NULL,
    descripcion VARCHAR(225),
    precio DECIMAL(10,2) NOT NULL,
    estado VARCHAR(1) DEFAULT '1',
    Categoria_idCategoria INT REFERENCES Categoria(idCategoria) ON DELETE SET NULL
);

CREATE TABLE DetallePedido (
    Producto_idProducto INT REFERENCES Producto(idProducto) ON DELETE CASCADE,
    Pedido_idPedido INT REFERENCES Pedido(idPedido) ON DELETE CASCADE,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (Producto_idProducto, Pedido_idPedido)
);

CREATE TABLE Factura (
    idFactura SERIAL PRIMARY KEY,
    numero_factura VARCHAR(45) UNIQUE NOT NULL,
    fecha_emision TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    subtotal DECIMAL(10,2) NOT NULL,
    descuento DECIMAL(10,2) DEFAULT 0.00,
    impuesto DECIMAL(10,2) NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    Pedido_idPedido INT UNIQUE REFERENCES Pedido(idPedido) ON DELETE CASCADE
);

CREATE TABLE Ingrediente (
    idIngrediente SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    unidad_medida VARCHAR(25) NOT NULL,
    estado VARCHAR(1) DEFAULT '1'
);

CREATE TABLE Inventario (
    idInventario SERIAL PRIMARY KEY,
    cantidad_actual DECIMAL(10,3) NOT NULL,
    cantidad_minima DECIMAL(10,3) NOT NULL,
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Ingrediente_idIngrediente INT UNIQUE REFERENCES Ingrediente(idIngrediente) ON DELETE CASCADE
);

CREATE TABLE Ingrediente_has_Producto (
    Ingrediente_idIngrediente INT REFERENCES Ingrediente(idIngrediente) ON DELETE CASCADE,
    Producto_idProducto INT REFERENCES Producto(idProducto) ON DELETE CASCADE,
    cantidad DECIMAL(10,3) NOT NULL,
    PRIMARY KEY (Ingrediente_idIngrediente, Producto_idProducto)
);