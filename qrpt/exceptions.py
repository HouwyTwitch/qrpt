class QrptError(Exception):
    """Base QRPT exception."""


class DependencyError(QrptError):
    """Raised when optional crypto backends are unavailable."""


class PayloadError(QrptError):
    """Raised when serialized payload is malformed."""
