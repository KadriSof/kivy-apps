from app.repositories.base_repository import BaseRepository


class DeviceRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)