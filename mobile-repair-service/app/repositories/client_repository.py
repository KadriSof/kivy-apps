"""Extends BaseRepository and can include additional client-specific methods if needed."""
from .base_repository import BaseRepository
from ..models.client import Client


class ClientRepository(BaseRepository):
    def __init__(self):
        super().__init__()

    def get_by_id(self, client_id, session):
        return session.query(Client).filter(Client.id == client_id).one_or_none()

    def filter_by_first_name(self, first_name, session):
        return session.query(Client).filter(Client.first_name.ilike(f'%{first_name}%')).all()

    def filter_by_last_name(self, last_name, session):
        return session.query(Client).filter(Client.last_name.ilike(f'%{last_name}%')).all()

    def filter_by_phone_number(self, phone_number, session):
        return session.query(Client).filter(Client.phone_number.ilike(f'%{phone_number}%')).all()
