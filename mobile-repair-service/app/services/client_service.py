"""Client business logic."""
from app.repositories.client_repository import ClientRepository
from app.entities.client import Client as ClientEntity
from app.models.client import Client as ClientModel
from app.database.session import get_session
from app.utils.session_manager import managed_session


class ClientService:
    def __init__(self):
        self.client_repository = ClientRepository()

    @staticmethod
    def _convert_to_entity(client: ClientModel):
        return ClientEntity(
            client_first_name=client.first_name,
            client_last_name=client.last_name,
            client_email=client.email,
            client_phone_number=client.phone_number
        )

    @staticmethod
    def _convert_from_entity(entity: ClientEntity):
        return ClientModel(
            first_name=entity.first_name,
            last_name=entity.last_name,
            email=entity.email,
            phone_number=entity.phone_number
        )

    def create_client(self, first_name, last_name, email, phone_number):
        session = get_session()
        try:
            new_client = ClientModel(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number)
            self.client_repository.add(new_client)
            return new_client

        except Exception as e:
            self.session.rollback()
            raise

        finally:
            self.session.close()

    @managed_session
    def get_client(self, client_id, session=None):
        client_model = self.client_repository.get(ClientModel, client_id, session=session)
        if client_model:
            return self._convert_from_entity(client_model)
        return None

    @managed_session
    def list_clients(self, session=None):
        clients = self.client_repository.list(ClientModel, session=session)
        return [self._convert_to_entity(client) for client in clients]
