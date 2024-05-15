from ..repositories.client_repository import ClientRepository
from ..models.client import Client


class ClientService:
    def __init__(self, session):
        self.client_repository = ClientRepository(session)

    def create_client(self, first_name, last_name, email, phone_number):
        new_client = Client(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number)
        self.client_repository.add(new_client)
        return new_client

    def get_client(self, client_id):
        return self.client_repository.get(Client, client_id)

    def list_clients(self):
        return self.client_repository.list(Client)
