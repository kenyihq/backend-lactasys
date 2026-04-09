from sqlalchemy import Column, ForeignKey, Numeric, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.db.base import Base

class Registro(Base):
    __tablename__ = "registros"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    ganadero_id = Column(UUID(as_uuid=True), ForeignKey("ganaderos.id"))
    planta_id = Column(UUID(as_uuid=True), ForeignKey("plantas.id"))
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"))

    litros = Column(Numeric)
    fecha_hora = Column(DateTime, default=datetime.utcnow)

    tipo_registro = Column(String, default="normal")