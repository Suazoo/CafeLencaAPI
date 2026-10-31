CREATE OR REPLACE FUNCTION public.registrar_pedido(payload jsonb)
RETURNS jsonb
LANGUAGE plpgsql
SECURITY INVOKER
SET search_path = public
AS $$
DECLARE
    linea record;
    producto public.producto%ROWTYPE;
    inventario public.inventario%ROWTYPE;
    componente public.ingrediente_has_producto%ROWTYPE;
    pedido_id integer;
    subtotal numeric(10, 2) := 0;
    descuento numeric(10, 2);
    tasa_impuesto numeric(6, 5);
    impuesto numeric(10, 2);
    total numeric(10, 2);
    precio_producto numeric(10, 2);
    requerido numeric(10, 3);
    alertas text[] := ARRAY[]::text[];
    numero_factura text;
BEGIN
    IF jsonb_typeof(payload->'detalles') <> 'array'
       OR jsonb_array_length(payload->'detalles') = 0 THEN
        RAISE EXCEPTION 'El pedido debe contener al menos un detalle.'
            USING ERRCODE = 'P0001';
    END IF;

    IF EXISTS (
        SELECT 1
        FROM jsonb_to_recordset(payload->'detalles')
             AS detalle(producto_id integer, cantidad integer)
        GROUP BY producto_id
        HAVING count(*) > 1
    ) THEN
        RAISE EXCEPTION 'No repitas productos en los detalles del pedido; suma sus cantidades.'
            USING ERRCODE = 'P0001';
    END IF;

    FOR linea IN
        SELECT producto_id, cantidad
        FROM jsonb_to_recordset(payload->'detalles')
             AS detalle(producto_id integer, cantidad integer)
    LOOP
        IF linea.producto_id IS NULL OR linea.cantidad IS NULL OR linea.cantidad <= 0 THEN
            RAISE EXCEPTION 'Cada detalle debe tener un producto y una cantidad mayor que cero.'
                USING ERRCODE = 'P0001';
        END IF;

        SELECT *
        INTO producto
        FROM public.producto
        WHERE idproducto = linea.producto_id
        FOR UPDATE;

        IF NOT FOUND THEN
            RAISE EXCEPTION 'No existe el producto %.', linea.producto_id
                USING ERRCODE = 'P0001';
        END IF;

        IF upper(trim(producto.estado)) NOT IN ('1', 'A', 'ACTIVO') THEN
            RAISE EXCEPTION 'El producto "%" está inactivo.', producto.nombre
                USING ERRCODE = 'P0001';
        END IF;

        subtotal := subtotal + round(producto.precio * linea.cantidad, 2);
    END LOOP;

    descuento := round(COALESCE((payload->>'descuento')::numeric, 0), 2);
    IF descuento < 0 OR descuento > subtotal THEN
        RAISE EXCEPTION 'El descuento debe estar entre cero y el subtotal.'
            USING ERRCODE = 'P0001';
    END IF;

    tasa_impuesto := COALESCE((payload->>'tasa_impuesto')::numeric, 0.15);
    IF tasa_impuesto < 0 OR tasa_impuesto > 1 THEN
        RAISE EXCEPTION 'La tasa de impuesto debe estar entre cero y uno.'
            USING ERRCODE = 'P0001';
    END IF;

    impuesto := round((subtotal - descuento) * tasa_impuesto, 2);
    total := round(subtotal - descuento + impuesto, 2);

    IF payload->>'cliente_id' IS NOT NULL
       AND NOT EXISTS (
           SELECT 1 FROM public.cliente WHERE idcliente = (payload->>'cliente_id')::integer
       ) THEN
        RAISE EXCEPTION 'El cliente no existe.' USING ERRCODE = 'P0001';
    END IF;
    IF payload->>'mesa_id' IS NOT NULL
       AND NOT EXISTS (
           SELECT 1 FROM public.mesa WHERE idmesa = (payload->>'mesa_id')::integer
       ) THEN
        RAISE EXCEPTION 'La mesa no existe.' USING ERRCODE = 'P0001';
    END IF;
    IF payload->>'metodo_pago_id' IS NOT NULL
       AND NOT EXISTS (
           SELECT 1 FROM public.metodopago WHERE idmetodopago = (payload->>'metodo_pago_id')::integer
       ) THEN
        RAISE EXCEPTION 'El método de pago no existe.' USING ERRCODE = 'P0001';
    END IF;
    IF payload->>'empleado_id' IS NOT NULL
       AND NOT EXISTS (
           SELECT 1 FROM public.empleado WHERE idempleado = (payload->>'empleado_id')::integer
       ) THEN
        RAISE EXCEPTION 'El empleado no existe.' USING ERRCODE = 'P0001';
    END IF;

    INSERT INTO public.pedido (
        cliente_idcliente,
        mesa_idmesa,
        metodopago_idmetodopago,
        empleado_idempleado,
        estado
    )
    VALUES (
        (payload->>'cliente_id')::integer,
        (payload->>'mesa_id')::integer,
        (payload->>'metodo_pago_id')::integer,
        (payload->>'empleado_id')::integer,
        '1'
    )
    RETURNING idpedido INTO pedido_id;

    FOR linea IN
        SELECT producto_id, cantidad
        FROM jsonb_to_recordset(payload->'detalles')
             AS detalle(producto_id integer, cantidad integer)
    LOOP
        SELECT precio
        INTO precio_producto
        FROM public.producto
        WHERE idproducto = linea.producto_id;

        FOR componente IN
            SELECT *
            FROM public.ingrediente_has_producto
            WHERE producto_idproducto = linea.producto_id
        LOOP
            SELECT *
            INTO inventario
            FROM public.inventario
            WHERE ingrediente_idingrediente = componente.ingrediente_idingrediente
            FOR UPDATE;

            IF NOT FOUND THEN
                RAISE EXCEPTION 'Falta configurar inventario para el ingrediente ID %.',
                    componente.ingrediente_idingrediente
                    USING ERRCODE = 'P0001';
            END IF;

            requerido := componente.cantidad * linea.cantidad;
            IF inventario.cantidad_actual < requerido THEN
                RAISE EXCEPTION 'Inventario insuficiente para el ingrediente ID %; se requiere % y hay %.',
                    componente.ingrediente_idingrediente,
                    requerido,
                    inventario.cantidad_actual
                    USING ERRCODE = 'P0001';
            END IF;

            UPDATE public.inventario AS inv
            SET cantidad_actual = inv.cantidad_actual - requerido
            WHERE inv.idinventario = inventario.idinventario;

            IF inventario.cantidad_actual - requerido <= inventario.cantidad_minima THEN
                alertas := array_append(
                    alertas,
                    format('Inventario bajo para ingrediente ID %s.', componente.ingrediente_idingrediente)
                );
            END IF;
        END LOOP;

        INSERT INTO public.detallepedido (
            producto_idproducto,
            pedido_idpedido,
            cantidad,
            precio_unitario
        )
        VALUES (
            linea.producto_id,
            pedido_id,
            linea.cantidad,
            precio_producto
        );
    END LOOP;

    numero_factura := format('CL-%s-%s', to_char(current_date, 'YYYYMMDD'), lpad(pedido_id::text, 6, '0'));
    INSERT INTO public.factura (
        numero_factura,
        subtotal,
        descuento,
        impuesto,
        total,
        pedido_idpedido
    )
    VALUES (numero_factura, subtotal, descuento, impuesto, total, pedido_id);

    RETURN jsonb_build_object(
        'pedido_id', pedido_id,
        'alertas_inventario', to_jsonb(alertas)
    );
END;
$$;
