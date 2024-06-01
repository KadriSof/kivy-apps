from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ServiceResponse:
    success: bool
    message: str
    data: Optional[object] = field(default=None)
