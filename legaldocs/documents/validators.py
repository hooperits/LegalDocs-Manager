"""
File upload validators for document security.

Provides validation for file uploads including:
- MIME type validation using python-magic
- File size validation
"""

import magic
from django.conf import settings
from django.core.exceptions import ValidationError


def validate_file_type(file) -> None:
    """
    Validate that the uploaded file is an allowed MIME type.

    Uses python-magic to detect the actual file type by reading
    the file's magic bytes, not just the extension.

    Args:
        file: Django UploadedFile object to validate.

    Raises:
        ValidationError: If file type is not in ALLOWED_FILE_TYPES.
    """
    # Read first 2048 bytes to detect MIME type
    file_data = file.read(2048)
    file.seek(0)  # Reset file pointer for subsequent operations

    mime_type = magic.from_buffer(file_data, mime=True)

    allowed_types = getattr(settings, 'ALLOWED_FILE_TYPES', [
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'text/plain',
        'image/jpeg',
        'image/png',
    ])

    if mime_type not in allowed_types:
        raise ValidationError(
            f'Tipo de archivo no permitido: {mime_type}. '
            f'Tipos permitidos: PDF, DOC, DOCX, TXT, JPG, PNG.'
        )


def validate_file_size(file) -> None:
    """
    Validate that the uploaded file does not exceed the maximum size.

    Args:
        file: Django UploadedFile object to validate.

    Raises:
        ValidationError: If file size exceeds MAX_UPLOAD_SIZE setting.
    """
    max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 10 * 1024 * 1024)  # Default 10MB

    if file.size > max_size:
        max_size_mb = max_size / (1024 * 1024)
        file_size_mb = file.size / (1024 * 1024)
        raise ValidationError(
            f'El archivo excede el tamaño máximo de {max_size_mb:.0f} MB. '
            f'Tamaño del archivo: {file_size_mb:.2f} MB.'
        )


def validate_file_upload(file) -> None:
    """
    Validate both file type and size for uploads.

    Combines validate_file_type and validate_file_size for convenience.

    Args:
        file: Django UploadedFile object to validate.

    Raises:
        ValidationError: If file type is invalid or size exceeds limit.
    """
    validate_file_size(file)
    validate_file_type(file)
