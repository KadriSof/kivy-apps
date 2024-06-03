from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class DiagnosticReport:
    device_id: int
    report_date: datetime
    report_details: str
    resolved: bool = False
    report_id: Optional[int] = field(default=None)
