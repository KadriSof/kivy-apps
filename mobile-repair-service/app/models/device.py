from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base


class Device(Base):
    __tablename__ = 'devices'
    id = Column(Integer, primary_key=True)
    type = Column(String(20), nullable=False)
    brand = Column(String(50), nullable=False)
    model = Column(String(100), nullable=False)
    fault_type = Column(String(50), nullable=False)
    fault_code = Column(String(50), nullable=False)
    fault_level = Column(String(50), nullable=False)
    registered_at = Column(DateTime(timezone=True), server_default=func.sysdate())
    delivered_at = Column(DateTime(timezone=True), onupdate=func.sysdate())
    status = Column(String(20), nullable=False, default='pending')

    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    client = relationship('Client', back_populates='devices', lazy='joined')

    # diagnostic_report = relationship('DiagnosticReport', uselist=False, backref='device')
    diagnostic_report = relationship('DiagnosticReport', uselist=False, back_populates='device')

    def __repr__(self):
        return f"<Device(id={self.id}, brand={self.brand}, model={self.model}, status={self.status})>"
