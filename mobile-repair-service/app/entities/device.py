"""-DEVICE ENTITY-"""


class Device:
    def __init__(self, device_type, device_brand: str, device_model: str, device_status: str):
        # TODO: Figure out how to transfer the 'id' from the entity to the model and vice-versa.
        self.device_type = device_type
        self.device_brand = device_brand
        self.device_model = device_model
        self.device_status = device_status

    def update_info(self, device_type: str = None, device_brand: str = None, device_model: str = None, device_status: str = None):
        """Update the device information."""
        if device_type:
            self.device_type = device_type
        if device_brand:
            self.device_brand = device_brand
        if device_model:
            self.device_model = device_model
        if device_status:
            self.device_status = device_status

    def __str__(self):
        """String representation of the device."""
        return f"Device brand={self.device_brand}, model={self.device_model}, status={self.device_status})"

    def get_summary(self):
        """Return a summary of the device details."""
        return {
            'type': self.device_type,
            'brand': self.device_brand,
            'model': self.device_model,
            'status': self.device_status
        }
