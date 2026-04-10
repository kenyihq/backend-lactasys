from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base import Base

class PagoRegistro(Base):
    __tablename__ = "pago_registro"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    pago_id = Column(UUID(as_uuid=True), ForeignKey("pagos.id"))
    registro_id = Column(UUID(as_uuid=True), ForeignKey("registros.id"))