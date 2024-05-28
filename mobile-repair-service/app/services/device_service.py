import logging

from app.entities.device import Device as DeviceEntity
from app.models.device import Device as DeviceModel
from app.repositories.device_repository import DeviceRepository
from app.utils.session_manager import managed_session


class DeviceService:
    def __init__(self):
        self.device_repository = DeviceRepository()

    @staticmethod
    def _convert_to_entity(device: DeviceModel):
        return DeviceEntity(
            device_id=device.id,
            device_type=device.type,
            device_brand=device.brand,
            device_model=device.model,
            fault_code=device.fault_code,
            fault_type=device.fault_type,
            fault_level=device.fault_level,
            device_status=device.status
        )

    @staticmethod
    def _convert_to_model(device_entity):
        return DeviceModel(
            type=device_entity.device_type,
            brand=device_entity.device_brand,
            model=device_entity.device_model,
            fault_type=device_entity.fault_type,
            fault_code=device_entity.fault_code,
            fault_level=device_entity.fault_level,
            status=device_entity.device_status
        )

    @managed_session
    def update_device_status(self, device_id, new_status, session=None):
        device_model = self.device_repository.get_by_id(device_id, session=session)
        if device_model:
            device_model.status = new_status
            self.device_repository.update(device_model, session)
            logging.info(f"Device Service: Updated device {device_id} status to {new_status}")
            return self._convert_to_entity(device_model)
        else:
            logging.info(f"Device Service: Failed to update device {device_id}")
            return None

    @managed_session
    def register_device(self, device_entity: DeviceEntity, session=None):
        device_model = self._convert_to_model(device_entity)
        self.device_repository.add(device_model, session=session)
        device_entity.device_id = device_model.id
        logging.info("Device Service: Registered {}".format(device_model))
        return device_entity

    # TODO: Delete this method since probably it won't be used.
    @managed_session
    def get_device(self, device_id, session=None):
        device_model = self.device_repository.get(DeviceModel, device_id, session)
        if device_model:
            return self._convert_to_entity(device_model)
        return None

    @managed_session
    def list_devices(self, session=None):
        devices = self.device_repository.list(DeviceModel, session)
        return [self._convert_to_entity(device) for device in devices]

    @managed_session
    def delete_device(self, device_id, session=None):
        device = self.get_device(device_id, session)
        if device:
            self.device_repository.delete(device, session)

    @managed_session
    def list_devices_by_status(self, status, session=None):
        devices = self.device_repository.filter_by_status(status, session)
        return [self._convert_to_entity(device) for device in devices]
