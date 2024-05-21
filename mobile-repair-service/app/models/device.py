from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Device(Base):
    __tablename__ = 'devices'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    type = Column(String(10), nullable=False)
    brand = Column(String(50), nullable=False)
    model = Column(String(100), nullable=False)
    status = Column(String(10), nullable=False)

    client = relationship('Client', back_populates='devices', lazy='joined')
