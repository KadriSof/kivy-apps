from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class DiagnosticReport(Base):
    __tablename__ = 'diagnostic_reports'
    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey('devices.id'), nullable=False)
    report_date = Column(DateTime(timezone=True), nullable=False)
    report_details = Column(String(255), nullable=False)
    resolved = Column(Boolean, default=False)

    device = relationship('Device', back_populates='diagnostic_report')

    def __repr__(self):
        return f"<DiagnosticReport(id={self.id}, device_id={self.device_id}, resolved={self.resolved})>"
