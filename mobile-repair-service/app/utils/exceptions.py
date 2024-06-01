class ValidationError(Exception):
    """Raised when there is a validation error."""
    def __init__(self, message="Validation failed", errors=None):
        super().__init__(message)
        self.errors = errors if errors is not None else {}


class ServiceError(Exception):
    """Raised when there is an error in the service layer."""
    def __init__(self, message="Service layer error", details=None):
        super().__init__(message)
        self.details = details


class DatabaseError(Exception):
    """Raised when there is a database error."""
    def __init__(self, message="Database operation failed", original_exception=None):
        super().__init__(message)
        self.original_exception = original_exception


class NotFoundError(ServiceError):
    """Raised when an entity is not found."""
    def __init__(self, entity_name="Entity", entity_id=None):
        message = f"{entity_name} with ID {entity_id} not found" if entity_id else f"{entity_name} not found"
        super().__init__(message)


class DuplicateEntryError(ServiceError):
    """Raised when attempting to create a duplicate entry."""
    def __init__(self, entity_name="Entity", unique_field="field"):
        message = f"{entity_name} with the same {unique_field} already exists."
        super().__init__(message)


class UnauthorizedError(ServiceError):
    """Raised when an unauthorized action is attempted."""
    def __init__(self, action="Action"):
        message = f"Unauthorized attempt to {action}."
        super().__init__(message)
