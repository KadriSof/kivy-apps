from .base_repository import BaseRepository
from ..models.client import Client


class ClientRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)
