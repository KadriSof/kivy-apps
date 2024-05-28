from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True)
    phone_number = Column(String(20), unique=True)

    devices = relationship('Device', back_populates='client')

    def __repr__(self):
        return (f"<Client(id={self.id}, first name={self.first_name}, last name={self.last_name}"
                f", phone_number={self.phone_number})>")
