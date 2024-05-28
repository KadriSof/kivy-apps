"""-DEVICE ENTITY-"""


class Client:
    def __init__(self, client_first_name: str, client_last_name: str, client_email: str, client_phone_number: str):
        self.first_name = client_first_name
        self.last_name = client_last_name
        self.email = client_email
        self.phone_number = client_phone_number

    def update_info(self, client_first_name: str = None, client_last_name: str = None, client_email: str = None,
                    client_phone_number: str = None):
        """Update the client information."""
        if client_first_name:
            self.first_name = client_first_name
        if client_last_name:
            self.last_name = client_last_name
        if client_email:
            self.email = client_email
        if client_phone_number:
            self.phone_number = client_phone_number

    def __str__(self):
        """String representation of the client."""
        return (f"Client first name={self.first_name}, last name={self.last_name}, email={self.email}, "
                f"phone={self.phone_number})")

    def get_summary(self):
        """Return a summary of the device details."""
        return {
            'type': self.device_type,
            'brand': self.device_brand,
            'model': self.device_model,
            'status': self.device_status
        }
