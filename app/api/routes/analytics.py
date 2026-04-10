from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.api.deps import get_db
from app.models.pago import Pago

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