"""-DEVICE ENTITY-"""


class Device:
    def __init__(self, device_type: str, device_brand: str, device_model: str, fault_type: str,
                 fault_code: str, fault_level: str, device_status: str = "Defective", device_id: int = None):
        self.device_id = device_id
        self.device_type = device_type
        self.device_brand = device_brand
        self.device_model = device_model
        self.fault_type = fault_type
        self.fault_code = fault_code
        self.fault_level = fault_level
        self.device_status = device_status

    def update_info(self, device_type: str = None, device_brand: str = None, device_model: str = None,
                    fault_type: str = None, fault_code: str = None, fault_level: str = None,device_status: str = None):
        """Update the device information."""
        if device_type:
            self.device_type = device_type
        if device_brand:
            self.device_brand = device_brand
        if device_model:
            self.device_model = device_model
        if fault_type:
            self.fault_type = fault_type
        if fault_code:
            self.fault_code = fault_code
        if fault_level:
            self.fault_level = fault_level
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
