from pydantic import BaseModel
from uuid import UUID

class RegistroCreate(BaseModel):
    ganadero_id: UUID
    planta_id: UUID
    litros: float