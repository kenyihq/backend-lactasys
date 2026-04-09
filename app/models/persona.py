from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base import Base

class Persona(Base):
    __tablename__ = "personas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tipo_documento = Column(String)
    numero_documento = Column(String)
    nombres = Column(String)
    apellidos = Column(String)
    telefono = Column(String)
    estado = Column(Boolean, default=True)