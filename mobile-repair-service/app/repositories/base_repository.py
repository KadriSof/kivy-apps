"""Manages basic CRUD operations and can be extended for specific models."""
from sqlalchemy.orm import Session


class BaseRepository:
    def __init__(self):
        pass

    def add(self, entity, session: Session):
        session.add(entity)
        session.commit()

    def get(self, entity_class, entity_id, session: Session):
        return session.query(entity_class).get(entity_id)

    def list(self, entity_class, session: Session):
        return session.query(entity_class).all()

    def delete(self, entity: object, session: Session) -> None:
        session.delete(entity)
        session.commit()
