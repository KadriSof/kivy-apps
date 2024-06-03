from app.repositories.base_repository import BaseRepository
from app.models.diagnostic_report import DiagnosticReport


class DiagnosticReportRepository(BaseRepository):
    def __init__(self):
        super().__init__()

    def get_by_id(self, report_id, session):
        return session.query(DiagnosticReport).filter(DiagnosticReport.id == report_id).one_or_none()

    def get_by_device_id(self, device_id, session):
        return session.query(DiagnosticReport).filter(DiagnosticReport.device_id == device_id).all()

    def update(self, report, session):
        session.add(report)
        session.commit()
