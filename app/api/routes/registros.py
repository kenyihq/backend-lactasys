from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.api.deps import get_current_user

from app.api.deps import get_db
from app.schemas.registro import RegistroCreate
from app.models.registro import Registro
from app.models.usuario_planta import UsuarioPlanta
from app.models.cliente_planta import ClientePlanta
from app.models.rol import Rol

router = APIRouter()

@router.post("/")
def crear_registro(
    data: RegistroCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user["user_id"]
    es_superadmin = current_user["es_superadmin"]

    # 👑 superadmin bypass
    if es_superadmin:
        tipo = "admin_override"
    else:
        relacion = db.query(UsuarioPlanta).filter(
            UsuarioPlanta.usuario_id == user_id,
            UsuarioPlanta.planta_id == data.planta_id
        ).first()

        if not relacion:
            raise HTTPException(status_code=403, detail="Usuario no pertenece a la planta")

        rol = db.query(Rol).filter(Rol.id == relacion.rol_id).first()

        if rol.nombre not in ["lechero", "admin_planta"]:
            raise HTTPException(status_code=403, detail="Rol no autorizado")

        tipo = "admin_override" if rol.nombre == "admin_planta" else "normal"

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