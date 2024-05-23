from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base


class Device(Base):
    __tablename__ = 'devices'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    type = Column(String(20), nullable=False)
    brand = Column(String(50), nullable=False)
    model = Column(String(100), nullable=False)
    fault_type = Column(String(50), nullable=False)
    fault_code = Column(String(50), nullable=False)
    fault_level = Column(String(50), nullable=False)
    registration_time = Column(DateTime, server_default=func.now())
    delivery_time = Column(DateTime, onupdate=func.now())
    status = Column(String(20), nullable=False, default='pending')
    diagnostic_report_id = Column(Integer, ForeignKey('diagnostic_reports.id'), nullable=True)

    client = relationship('Client', back_populates='devices', lazy='joined')
    diagnostic_report = relationship('DiagnosticReport', back_populates='device')

    def __repr__(self):
        return f"<Device(id={self.id}, brand={self.brand}, model={self.model}, status={self.status})>"
