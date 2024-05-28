from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base


class DiagnosticReport(Base):
    __tablename__ = 'diagnostic_reports'
    id = Column(Integer, primary_key=True, index=True)
    report = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # device_id = Column(Integer, ForeignKey('devices.id'), nullable=False)
    device_id = Column(Integer, ForeignKey('devices.id'), nullable=False)
    device = relationship('Device', back_populates='diagnostic_report')

    def __repr__(self):
        return f"<DiagnosticReport(id={self.id})>"
