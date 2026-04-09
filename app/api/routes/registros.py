from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.api.deps import get_db
from app.schemas.registro import RegistroCreate
from app.models.registro import Registro
from app.models.usuario_planta import UsuarioPlanta
from app.models.cliente_planta import ClientePlanta

router = APIRouter()

@router.post("/")
def crear_registro(
    data: RegistroCreate,
    user_id: str,
    db: Session = Depends(get_db)
):

    # 🔒 validar usuario pertenece a planta
    user_planta = db.query(UsuarioPlanta).filter(
        UsuarioPlanta.usuario_id == user_id,
        UsuarioPlanta.planta_id == data.planta_id
    ).first()

    if not user_planta:
        raise HTTPException(status_code=403, detail="Usuario no pertenece a la planta")

    # 🔒 validar ganadero pertenece a planta
    ganadero_planta = db.query(ClientePlanta).filter(
        ClientePlanta.ganadero_id == data.ganadero_id,
        ClientePlanta.planta_id == data.planta_id
    ).first()

    if not ganadero_planta:
        raise HTTPException(status_code=400, detail="Ganadero no pertenece a la planta")

    # 🔥 crear registro
    nuevo = Registro(
        ganadero_id=data.ganadero_id,
        planta_id=data.planta_id,
        usuario_id=user_id,
        litros=data.litros,
        fecha_hora=datetime.utcnow(),
        tipo_registro="normal"
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return {
        "id": str(nuevo.id),
        "litros": float(nuevo.litros)
    }