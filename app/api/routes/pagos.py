from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.api.deps import get_db, get_current_user
from app.models.registro import Registro
from app.models.pago import Pago
from app.models.pago_registro import PagoRegistro

router = APIRouter()

@router.post("/")
def crear_pago(
    data: PagoCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user["user_id"]

    # 🔍 obtener registros no pagados
    registros = (
        db.query(Registro)
        .outerjoin(PagoRegistro, Registro.id == PagoRegistro.registro_id)
        .filter(
            Registro.planta_id == data.planta_id,
            Registro.fecha_hora >= data.fecha_inicio,
            Registro.fecha_hora <= data.fecha_fin,
            PagoRegistro.id == None
        )
        .all()
    )

    if not registros:
        raise HTTPException(status_code=400, detail="No hay registros para pagar")

    total_litros = sum([float(r.litros) for r in registros])
    total_pago = total_litros * data.precio_por_litro

    # 💰 crear pago
    pago = Pago(
        planta_id=data.planta_id,
        fecha_inicio=data.fecha_inicio,
        fecha_fin=data.fecha_fin,
        precio_por_litro=data.precio_por_litro,
        total_litros=total_litros,
        total_pago=total_pago,
        created_by=user_id
    )

    db.add(pago)
    db.commit()
    db.refresh(pago)

    # 🔗 vincular registros
    for r in registros:
        pr = PagoRegistro(
            pago_id=pago.id,
            registro_id=r.id
        )
        db.add(pr)

    db.commit()

    return {
        "pago_id": str(pago.id),
        "total_litros": total_litros,
        "total_pago": total_pago
    }