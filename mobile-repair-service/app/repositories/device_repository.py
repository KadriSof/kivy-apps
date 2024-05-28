from app.repositories.base_repository import BaseRepository
from app.models.device import Device


class DeviceRepository(BaseRepository):
    def __init__(self):
        super().__init__()

    def get_by_id(self, device_id, session):
        return session.query(Device).filter(Device.id == device_id).one_or_none()

    def filter_by_status(self, status, session):
        return session.query(Device).filter(Device.status == status).all()

    def update(self, device, session):
        session.add(device)
        session.commit()