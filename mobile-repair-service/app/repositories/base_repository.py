"""Manages basic CRUD operations and can be extended for specific models."""
from sqlalchemy.orm import Session


class BaseRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, entity):
        self.session.add(entity)
        self.session.commit()

    def get(self, entity_class, entity_id):
        return self.session.query(entity_class).get(entity_id)

    def list(self, entity_class):
        return self.session.query(entity_class).all()

    def delete(self, entity):
        self.session.delete(entity)
        self.session.commit()