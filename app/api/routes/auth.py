from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.usuario import Usuario
from app.models.persona import Persona
from app.models.usuario_planta import UsuarioPlanta
from app.models.planta import Planta

router = APIRouter()

@router.post("/login")
def login(documento: str, password: str, db: Session = Depends(get_db)):

    user = (
        db.query(Usuario)
        .join(Persona, Usuario.persona_id == Persona.id)
        .filter(Persona.numero_documento == documento)
        .first()
    )

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if user.password != password:
        raise HTTPException(status_code=401, detail="Password incorrecto")

    return {
        "user_id": str(user.id),
        "es_superadmin": user.es_superadmin
    }


@router.get("/mis-plantas/{user_id}")
def mis_plantas(user_id: str, db: Session = Depends(get_db)):

    user = db.query(Usuario).filter(Usuario.id == user_id).first()

    if user.es_superadmin:
        plantas = db.query(Planta).all()
    else:
        plantas = (
            db.query(Planta)
            .join(UsuarioPlanta, UsuarioPlanta.planta_id == Planta.id)
            .filter(UsuarioPlanta.usuario_id == user_id)
            .all()
        )

    return [
        {
            "id": str(p.id),
            "nombre": p.nombre,
            "codigo": p.codigo
        }
        for p in plantas
    ]