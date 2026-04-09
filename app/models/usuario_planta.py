from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base import Base

class UsuarioPlanta(Base):
    __tablename__ = "usuario_planta"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"))
    planta_id = Column(UUID(as_uuid=True), ForeignKey("plantas.id"))
    rol_id = Column(UUID(as_uuid=True))