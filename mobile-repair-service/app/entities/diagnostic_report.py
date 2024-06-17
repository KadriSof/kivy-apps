from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class DiagnosticReport:
    report_date: datetime = field(default=None, init=False)
    report_details: str = ''
    resolved: bool = False
    report_id: Optional[int] = field(default=None)
    device_id: Optional[int] = field(default=None)
