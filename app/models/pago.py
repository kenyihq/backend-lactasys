from sqlalchemy import Column, ForeignKey, Numeric, Date, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.db.base import Base

class Pago(Base):
    __tablename__ = "pagos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    ganadero_id = Column(UUID(as_uuid=True), ForeignKey("ganaderos.id"))
    planta_id = Column(UUID(as_uuid=True), ForeignKey("plantas.id"))

    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)

    precio_por_litro = Column(Numeric)
    total_litros = Column(Numeric)
    total_pago = Column(Numeric)

    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True))