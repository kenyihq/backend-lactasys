from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.api.deps import get_db
from app.models.pago import Pago
from app.models.planta import Planta

router = APIRouter()

@router.get("/resumen")
def resumen(db: Session = Depends(get_db)):
    result = db.query(
        func.sum(Pago.total_litros),
        func.sum(Pago.total_pago),
        func.count(Pago.id)
    ).first()

    return {
        "total_litros": float(result[0] or 0),
        "total_pago": float(result[1] or 0),
        "cantidad_pagos": result[2]
    }


@router.get("/por-planta")
def por_planta(db: Session = Depends(get_db)):
    result = db.query(
        Planta.nombre,
        func.sum(Pago.total_litros),
        func.sum(Pago.total_pago)
    ).join(Planta, Pago.planta_id == Planta.id)\
     .group_by(Planta.nombre)\
     .all()

    return [
        {
            "planta": r[0],
            "litros": float(r[1] or 0),
            "total": float(r[2] or 0)
        }
        for r in result
    ]