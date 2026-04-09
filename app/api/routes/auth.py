from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.usuario import Usuario
from app.models.persona import Persona

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