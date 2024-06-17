import logging

from pymysql import IntegrityError
from sqlalchemy.exc import SQLAlchemyError

from app.entities.device import Device as DeviceEntity
from app.models.device import Device as DeviceModel
from app.repositories.device_repository import DeviceRepository
from app.utils.response import ServiceResponse
from app.utils.session_manager import managed_session
from app.utils.exceptions import DatabaseError, ServiceError, NotFoundError


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
            device_status=device.status,
            client_id=device.client_id
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
            status=device_entity.device_status,
            client_id=device_entity.client_id
        )

    @managed_session
    def register_device(self, device_entity: DeviceEntity, session=None) -> ServiceResponse:
        device_model = self._convert_to_model(device_entity)

        try:
            self.device_repository.add(device_model, session=session)
            device_entity.device_id = device_model.id
            logging.info(f"Device Service: Registered device: {device_model}")
            return ServiceResponse(success=True, message="Device registered successfully!", data=device_entity)

        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseError("Failed to register device due to database error.", original_exception=e)
        except Exception as e:
            session.rollback()
            ServiceResponse(success=False, message="An unexpected error occurred in the service layer.")
            raise ServiceError("An unexpected error occurred in the service layer", details=str(e))

    @managed_session
    def get_device(self, device_id, session=None):
        device_model = self.device_repository.get(DeviceModel, device_id, session=session)

        if not device_model:
            raise NotFoundError(entity_name="Device", entity_id=device_id)

        return self._convert_to_entity(device_model)

    @managed_session
    def list_devices(self, session=None):
        devices = self.device_repository.list(DeviceModel, session=session)
        return [self._convert_to_entity(device) for device in devices]

    @managed_session
    def delete_device(self, device_id, session=None):
        device = self.get_device(device_id, session=session)

        if device:
            self.device_repository.delete(device, session)

    @managed_session
    def list_devices_by_status(self, status, session=None):
        devices = self.device_repository.filter_by_status(status, session=session)
        return [self._convert_to_entity(device) for device in devices]

    @managed_session
    def update_device_status(self, device_id, new_status, session=None):
        device_model = self.device_repository.update_field(device_id, "status", new_status, session=session)

        if not device_model:
            raise NotFoundError(entity_name="Device", entity_id=device_id)

        device_model.status = new_status
        self.device_repository.update(device_model, session=session)
        logging.info(f"DeviceService: Updated device: {device_id} 'status' to: {new_status}")
        return self._convert_to_entity(device_model)

    @managed_session
    def update_device_delivered_at(self, device_id, delivered_at, session=None):
        device_model = self.device_repository.update_field(device_id, "delivered_at", delivered_at, session=session)

        if not device_model:
            raise NotFoundError(entity_name="Device", entity_id=device_id)

        device_model.delivered_at = delivered_at
        self.device_repository.update(device_model, session=session)
        logging.info(f"DeviceService: Updated device: {device_id} 'delivered_at' to: {delivered_at}")
        return self._convert_to_entity(device_model)
