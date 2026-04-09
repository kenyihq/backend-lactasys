from sqlalchemy import Column, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base import Base

class ClientePlanta(Base):
    __tablename__ = "cliente_planta"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    ganadero_id = Column(UUID(as_uuid=True), ForeignKey("ganaderos.id"))
    planta_id = Column(UUID(as_uuid=True), ForeignKey("plantas.id"))

    estado = Column(Boolean, default=True)