"""Client business logic."""
from app.repositories.client_repository import ClientRepository
from app.models.client import Client
from app.database.session import get_session


class ClientService:
    def __init__(self, session):
        self.session = session
        self.client_repository = ClientRepository(self.session)

    def create_client(self, first_name, last_name, email, phone_number):
        session = get_session()
        try:
            new_client = Client(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number)
            self.client_repository.add(new_client)
            return new_client

        except Exception as e:
            self.session.rollback()
            raise

        finally:
            self.session.close()

    def get_client(self, client_id):
        return self.client_repository.get(Client, client_id)

    def list_clients(self):
        return self.client_repository.list(Client)
