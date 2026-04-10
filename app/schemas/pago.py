from pydantic import BaseModel
from uuid import UUID
from datetime import date

class PagoCreate(BaseModel):
    planta_id: UUID
    fecha_inicio: date
    fecha_fin: date
    precio_por_litro: float