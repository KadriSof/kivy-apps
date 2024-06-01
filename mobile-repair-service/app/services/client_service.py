"""Client business logic."""
import logging
from sqlalchemy.exc import IntegrityError
from pymysql.err import IntegrityError as PyMySQLError
from app.utils.exceptions import DatabaseError, ServiceError, NotFoundError, DuplicateEntryError

from app.repositories.client_repository import ClientRepository
from app.entities.client import Client as ClientEntity
from app.models.client import Client as ClientModel
from app.utils.response import ServiceResponse
from app.utils.session_manager import managed_session


class ClientService:
    def __init__(self):
        self.client_repository = ClientRepository()

    @staticmethod
    def _convert_to_entity(client: ClientModel):
        return ClientEntity(
            first_name=client.first_name,
            last_name=client.last_name,
            phone_number=client.phone_number,
            email=client.email,
            client_id=client.id,
        )

    @staticmethod
    def _convert_to_model(entity: ClientEntity):
        return ClientModel(
            first_name=entity.first_name,
            last_name=entity.last_name,
            email=entity.email,
            phone_number=entity.phone_number
        )

    @managed_session
    def register_client(self, client_entity: ClientEntity, session=None) -> ServiceResponse:
        client_model = self._convert_to_model(client_entity)

        try:
            self.client_repository.add(client_model, session=session)
            client_entity.client_id = client_model.id
            logging.info(f"Client Service: Registered client: {client_model}")
            return ServiceResponse(success=True, message="Client registered successfully!", data=client_entity)

        except IntegrityError as e:
            session.rollback()
            if (isinstance(e.orig, PyMySQLError)) and e.orig.args[0] == 1062:
                return ServiceResponse(success=False, message="The entered phone number is already registered.")
            return ServiceResponse(success=False, message="Failed to register client due to database error.")

        except Exception as e:
            session.rollback()
            ServiceResponse(success=False, message="An unexpected error occurred in the service layer.")

    @managed_session
    def get_client(self, client_id, session=None):
        client_model = self.client_repository.get(ClientModel, client_id, session=session)
        if client_model:
            return self._convert_to_entity(client_model)
        return None

    @managed_session
    def list_clients(self, session=None):
        clients = self.client_repository.list(ClientModel, session=session)
        return [self._convert_to_entity(client) for client in clients]
