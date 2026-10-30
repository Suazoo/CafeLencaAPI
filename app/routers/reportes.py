from datetime import date, datetime, time, timedelta
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.Factura import Factura
from app.models.Pedido import Pedido

router = APIRouter(prefix="/reportes", tags=["Reportes"])

@router.get("/ventas")
def reporte_ventas(
    desde: date | None = Query(default=None),
    hasta: date | None = Query(default=None),
    db: Session = Depends(get_db),
):
    if desde and hasta and desde > hasta:
        raise HTTPException(status_code=422, detail="'desde' no puede ser posterior a 'hasta'.")
    consulta = db.query(Factura)
    if desde:
        consulta = consulta.filter(Factura.fecha_emision >= datetime.combine(desde, time.min))
    if hasta:
        consulta = consulta.filter(Factura.fecha_emision < datetime.combine(hasta + timedelta(days=1), time.min))
    facturas = consulta.order_by(Factura.fecha_emision.desc()).all()
    total = sum((Decimal(str(f.total)) for f in facturas), Decimal("0.00"))
    por_dia = {}
    for factura in facturas:
        dia = factura.fecha_emision.date().isoformat()
        por_dia[dia] = por_dia.get(dia, Decimal("0.00")) + Decimal(str(factura.total))
    return {
        "desde": desde.isoformat() if desde else None,
        "hasta": hasta.isoformat() if hasta else None,
        "cantidad_facturas": len(facturas),
        "total_ventas": total,
        "ventas_por_dia": [{"fecha": dia, "total": importe} for dia, importe in sorted(por_dia.items())],
    }
