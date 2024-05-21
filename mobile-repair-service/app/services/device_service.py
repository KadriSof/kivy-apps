import logging

from app.entities.device import Device as DeviceEntity
from app.models.device import Device as DeviceModel
from app.repositories.device_repository import DeviceRepository


class DeviceService:
    def __init__(self, device_repository: DeviceRepository):
        self.device_repository = device_repository

    @staticmethod
    def _convert_to_entity(device: DeviceModel):
        return DeviceEntity(
            device_type=device.type,
            device_brand=device.brand,
            device_model=device.model,
            device_status=device.status
        )

    @staticmethod
    def _convert_to_model(device_entity):
        return DeviceModel(
            type=device_entity.device_type,
            brand=device_entity.device_brand,
            model=device_entity.device_model,
            status=device_entity.device_status
        )

    @staticmethod
    def create_device(device_type: str ,device_brand: str, device_model: str, device_status: str):
        device_entity = DeviceEntity(device_type, device_brand, device_model, device_status)
        device_model = DeviceModel(
            type=device_type,
            brand=device_brand,
            model=device_model,
            status=device_status
        )
        return device_entity

    # TODO: adjust the 'update_device' method accordingly.
    def update_device(self, device_id: int, name: str = None, brand: str = None, model: str = None, status: str = None):
        device_model = self.device_repository.get_by_id(device_id) # TODO: add 'get_by_id' method to 'DeviceRepository'
        if device_model:
            device_entity = DeviceEntity(
                device_type=device_model.type,
                device_brand=device_model.brand,
                device_model=device_model.model,
                device_status=device_model.status
            )
            device_entity.update_info(name, brand, model, status)
            # Update the device model with new data
            device_model.type = device_entity.device_type
            device_model.brand = device_entity.device_brand
            device_model.model = device_entity.device_model
            device_model.status = device_entity.device_status
            self.device_repository.update(device_model)
            return device_entity
        return None

    def register_device(self, device: DeviceEntity):
        device_object = self._convert_to_model(device)
        self.device_repository.add(device_object)
        logging.info("Device Service: Registered {}".format(device_object))
