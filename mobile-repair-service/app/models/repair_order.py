from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base
import datetime


class RepairOrder(Base):
    __tablename__ = 'repair_orders'
    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey('devices.id'))
    issue_description = Column(String(255), nullable=False)
    repair_date = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String(20), default='Pending')

    device = relationship('Device', back_populates='repairs')
