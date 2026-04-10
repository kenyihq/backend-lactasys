from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.api.deps import get_db
from app.models.pago import Pago
from app.models.planta import Planta
from app.models.ganadero import Ganadero
from app.models.persona import Persona

from app.api.deps import get_current_user
from app.models.usuario_planta import UsuarioPlanta


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

@router.get("/top-ganaderos")
def top_ganaderos(db: Session = Depends(get_db)):
    result = db.query(
        Persona.nombres,
        func.sum(Pago.total_litros).label("litros")
    ).join(Ganadero, Pago.ganadero_id == Ganadero.id)\
     .join(Persona, Ganadero.persona_id == Persona.id)\
     .group_by(Persona.nombres)\
     .order_by(func.sum(Pago.total_litros).desc())\
     .limit(5)\
     .all()

    return [
        {
            "ganadero": r[0],
            "litros": float(r[1])
        }
        for r in result
    ]


@router.get("/dashboard")
def dashboard(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user_id = current_user["user_id"]
    es_superadmin = current_user["es_superadmin"]

    filtro_planta = None

    if es_superadmin:
        filtro_planta = None
    else:
        relaciones = db.query(UsuarioPlanta).filter(
            UsuarioPlanta.usuario_id == user_id
        ).all()

        if not relaciones:
            raise HTTPException(status_code=403, detail="Sin acceso")

        plantas_ids = [r.planta_id for r in relaciones]


    # resumen
    query = db.query(
        func.sum(Pago.total_litros),
        func.sum(Pago.total_pago),
        func.count(Pago.id)
    )

    if not es_superadmin:
        query = query.filter(Pago.planta_id.in_(plantas_ids))

    resumen = query.first()

    # por planta
    query = db.query(
        Planta.nombre,
        func.sum(Pago.total_litros),
        func.sum(Pago.total_pago)
    ).join(Planta, Pago.planta_id == Planta.id)

    if not es_superadmin:
        query = query.filter(Pago.planta_id.in_(plantas_ids))

    por_planta = query.group_by(Planta.nombre).all()

    # top ganaderos
    top = db.query(
        Persona.nombres,
        func.sum(Pago.total_litros)
    ).join(Ganadero, Pago.ganadero_id == Ganadero.id)\
     .join(Persona, Ganadero.persona_id == Persona.id)\
     .group_by(Persona.nombres)\
     .order_by(func.sum(Pago.total_litros).desc())\
     .limit(5)\
     .all()

    return {
        "resumen": {
            "total_litros": float(resumen[0] or 0),
            "total_pago": float(resumen[1] or 0),
            "cantidad_pagos": resumen[2]
        },
        "por_planta": [
            {
                "planta": r[0],
                "litros": float(r[1] or 0),
                "total": float(r[2] or 0)
            } for r in por_planta
        ],
        "top_ganaderos": [
            {
                "ganadero": r[0],
                "litros": float(r[1])
            } for r in top
        ]
    }