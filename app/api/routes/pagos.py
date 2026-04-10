from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy import cast, Date

from app.api.deps import get_db, get_current_user
from app.schemas.pago import PagoCreate
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
    registros_por_ganadero = (
        db.query(
            Registro.ganadero_id,
            func.sum(Registro.litros).label("total_litros")
        )
        .outerjoin(PagoRegistro, Registro.id == PagoRegistro.registro_id)
        .filter(
            Registro.planta_id == data.planta_id,
            cast(Registro.fecha_hora, Date) >= data.fecha_inicio,
            cast(Registro.fecha_hora, Date) <= data.fecha_fin,
            PagoRegistro.id == None
        )
        .group_by(Registro.ganadero_id)
        .all()
    )

    if not registros_por_ganadero:
        raise HTTPException(status_code=400, detail="No hay registros para pagar")

    for item in registros_por_ganadero:
        total_litros = float(item.total_litros)
        total_pago = total_litros * data.precio_por_litro

    # 💰 crear pago
    pagos_creados = []

    for item in registros_por_ganadero:
        total_litros = float(item.total_litros)
        total_pago = total_litros * data.precio_por_litro

        pago = Pago(
            ganadero_id=item.ganadero_id,
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

        pagos_creados.append(pago)

    # 🔗 vincular registros
    for pago in pagos_creados:
        registros = db.query(Registro).filter(
            Registro.ganadero_id == pago.ganadero_id,
            Registro.planta_id == data.planta_id
        ).all()

        for r in registros:
            db.add(PagoRegistro(
                pago_id=pago.id,
                registro_id=r.id
            ))

    db.commit()

    return {
        "pago_id": str(pago.id),
        "total_litros": total_litros,
        "total_pago": total_pago
    }