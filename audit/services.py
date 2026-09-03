from .models import AuditLog


def log_action(user, action: str, obj, details: str = ""):
    AuditLog.objects.create(
        user=user,
        action=action,
        object_repr=str(obj),
        details=details,
    )