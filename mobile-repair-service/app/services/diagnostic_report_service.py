import logging
from sqlalchemy.exc import SQLAlchemyError
from app.entities.diagnostic_report import DiagnosticReport as DiagnosticReportEntity
from app.models.diagnostic_report import DiagnosticReport as DiagnosticReportModel
from app.repositories.diagnostic_report_repository import DiagnosticReportRepository
from app.utils.session_manager import managed_session
from app.utils.exceptions import DatabaseError, ServiceError, NotFoundError
from app.utils.response import ServiceResponse


class DiagnosticReportService:
    def __init__(self):
        self.diagnostic_report_repository = DiagnosticReportRepository()

    @staticmethod
    def _convert_to_entity(report: DiagnosticReportModel):
        return DiagnosticReportEntity(
            report_id=report.id,
            device_id=report.device_id,
            report_date=report.report_date,
            report_details=report.report_details,
            resolved=report.resolved
        )

    @staticmethod
    def _convert_to_model(report_entity):
        return DiagnosticReportModel(
            id=report_entity.report_id,
            device_id=report_entity.device_id,
            report_date=report_entity.report_date,
            report_details=report_entity.report_details,
            resolved=report_entity.resolved
        )

    @managed_session
    def register_report(self, report_entity: DiagnosticReportEntity, session=None):
        report_model = self._convert_to_model(report_entity)

        try:
            self.diagnostic_report_repository.add(report_model, session=session)
            report_entity.report_id = report_model.id
            logging.info(f"DiagnosticReportService: Registered report: {report_model}")
            return ServiceResponse(success=True, message="Report registered successfully.", data=report_entity)

        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseError("Failed to register report", original_exception=e)

        except Exception as e:
            raise ServiceError("An unexpected error occurred in the service layer", details=str(e))

    @managed_session
    def get_report(self, report_id, session=None):
        report_model = self.diagnostic_report_repository.get_by_id(report_id, session=session)

        if not report_model:
            raise NotFoundError(entity_name="DiagnosticReport", entity_id=report_id)

        return self._convert_to_entity(report_model)

    @managed_session
    def get_reports_by_device(self, device_id, session=None):
        reports = self.diagnostic_report_repository.get_by_device_id(device_id, session=session)
        return [self._convert_to_entity(report) for report in reports]

    @managed_session
    def update_report(self, report_entity: DiagnosticReportEntity, session=None):
        report_model = self.diagnostic_report_repository.get_by_id(report_entity.report_id, session=session)

        if not report_model:
            raise NotFoundError(entity_name="DiagnosticReport", entity_id=report_entity.report_id)

        report_model.report_details = report_entity.report_details
        report_model.resolved = report_entity.resolved

        try:
            self.diagnostic_report_repository.update(report_model, session=session)
            logging.info(f"DiagnosticReportService: Updated report: {report_entity.report_id}")
            return ServiceResponse(success=True, message="Report updated successfully.", data=report_entity)

        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseError("Failed to update report", original_exception=e)

        except Exception as e:
            raise ServiceError("An unexpected error occurred in the service layer", details=str(e))
