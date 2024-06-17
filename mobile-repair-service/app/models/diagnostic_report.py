from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base


class DiagnosticReport(Base):
    __tablename__ = 'diagnostic_reports'
    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey('devices.id'), nullable=False)
    report_date = Column(DateTime(timezone=True), server_default=func.sysdate())
    report_details = Column(String(255), nullable=False)
    resolved = Column(Boolean, default=False)

    devices = relationship('Device', back_populates='diagnostic_reports')

    def __repr__(self):
        return (f"<DiagnosticReport(id={self.id}, "
                f"device_id={self.device_id}, "
                f"report_details={self.report_details}, "
                f"resolved={self.resolved})>")
