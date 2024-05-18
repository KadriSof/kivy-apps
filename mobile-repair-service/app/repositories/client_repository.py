"""Extends BaseRepository and can include additional client-specific methods if needed."""
from .base_repository import BaseRepository
from ..models.client import Client


class ClientRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)
