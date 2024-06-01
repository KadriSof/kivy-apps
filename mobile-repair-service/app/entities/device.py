from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Device:
    device_type: str = ''
    device_brand: str = ''
    device_model: str = ''
    fault_type: str = ''
    fault_code: str = ''
    fault_level: str = ''
    device_status: str = 'Defective'
    device_id: Optional[int] = field(default=None)
    client_id: Optional[int] = field(default=None)
