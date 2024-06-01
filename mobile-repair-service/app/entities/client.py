from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Client:
    first_name: str
    last_name: str
    phone_number: str
    email: str
    client_id: Optional[int] = field(default=None)
