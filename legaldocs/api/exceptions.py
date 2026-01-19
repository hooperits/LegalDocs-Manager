"""
Custom exception handling for the LegalDocs API.

Provides a custom DRF exception handler that translates error messages
to Spanish and formats field names in a user-friendly way.
"""

from rest_framework.views import exception_handler


# Field name translations (English -> Spanish)
FIELD_TRANSLATIONS = {
    'username': 'nombre de usuario',
    'email': 'correo electrónico',
    'password': 'contraseña',
    'password_confirm': 'confirmación de contraseña',
    'full_name': 'nombre completo',
    'identification_number': 'número de identificación',
    'phone': 'teléfono',
    'address': 'dirección',
    'notes': 'notas',
    'case_number': 'número de caso',
    'title': 'título',
    'description': 'descripción',
    'case_type': 'tipo de caso',
    'status': 'estado',
    'priority': 'prioridad',
    'start_date': 'fecha de inicio',
    'deadline': 'fecha límite',
    'closed_date': 'fecha de cierre',
    'assigned_to': 'asignado a',
    'client': 'cliente',
    'client_id': 'cliente',
    'document_type': 'tipo de documento',
    'file': 'archivo',
    'file_size': 'tamaño del archivo',
    'is_confidential': 'confidencial',
    'is_active': 'activo',
    'case': 'caso',
    'first_name': 'nombre',
    'last_name': 'apellido',
    'non_field_errors': 'errores generales',
    'detail': 'detalle',
}


# Common error message translations (English -> Spanish)
ERROR_TRANSLATIONS = {
    # Required/blank errors
    'This field is required.': 'Este campo es obligatorio.',
    'This field may not be blank.': 'Este campo no puede estar vacío.',
    'This field may not be null.': 'Este campo no puede ser nulo.',

    # Unique/existence errors
    'A user with that username already exists.': 'Ya existe un usuario con ese nombre de usuario.',
    'This field must be unique.': 'Este campo debe ser único.',
    'Object with this value already exists.': 'Ya existe un objeto con este valor.',

    # Validation errors
    'Enter a valid email address.': 'Ingrese una dirección de correo electrónico válida.',
    'Enter a valid URL.': 'Ingrese una URL válida.',
    'Enter a valid integer.': 'Ingrese un número entero válido.',
    'Enter a valid number.': 'Ingrese un número válido.',
    'Enter a valid date.': 'Ingrese una fecha válida.',
    'Enter a valid date/time.': 'Ingrese una fecha/hora válida.',
    'Date has wrong format.': 'El formato de fecha es incorrecto.',

    # Length errors
    'Ensure this field has at least {min_length} characters.':
        'Asegúrese de que este campo tenga al menos {min_length} caracteres.',
    'Ensure this field has no more than {max_length} characters.':
        'Asegúrese de que este campo no tenga más de {max_length} caracteres.',

    # Authentication errors
    'Unable to log in with provided credentials.':
        'No se puede iniciar sesión con las credenciales proporcionadas.',
    'User account is disabled.': 'La cuenta de usuario está deshabilitada.',
    'Authentication credentials were not provided.':
        'No se proporcionaron credenciales de autenticación.',
    'Invalid token.': 'Token inválido.',
    'Token has expired.': 'El token ha expirado.',

    # Permission errors
    'You do not have permission to perform this action.':
        'No tiene permiso para realizar esta acción.',

    # Object errors
    'Not found.': 'No encontrado.',
    'Invalid pk "{pk_value}" - object does not exist.':
        'ID inválido "{pk_value}" - el objeto no existe.',

    # Password errors
    'Passwords do not match.': 'Las contraseñas no coinciden.',
    'This password is too short.': 'Esta contraseña es demasiado corta.',
    'This password is too common.': 'Esta contraseña es muy común.',
    'This password is entirely numeric.': 'Esta contraseña es completamente numérica.',

    # Rate limiting
    'Request was throttled.': 'Solicitud limitada por exceso de intentos.',

    # File errors
    'The submitted data was not a file.': 'Los datos enviados no son un archivo.',
    'The submitted file is empty.': 'El archivo enviado está vacío.',
    'No file was submitted.': 'No se envió ningún archivo.',

    # Case specific
    'Case already closed': 'El caso ya está cerrado',
}


def translate_error_message(message: str) -> str:
    """
    Translate an error message from English to Spanish.

    Args:
        message: The error message in English.

    Returns:
        The translated message in Spanish, or the original if not found.
    """
    # Try exact match first
    if message in ERROR_TRANSLATIONS:
        return ERROR_TRANSLATIONS[message]

    # Try pattern matching for messages with variables
    for english, spanish in ERROR_TRANSLATIONS.items():
        if '{' in english:
            # Handle parameterized messages
            pattern = english.replace('{min_length}', '(\\d+)').replace('{max_length}', '(\\d+)')
            pattern = pattern.replace('{pk_value}', '(.+)')
            import re
            match = re.match(pattern, message)
            if match:
                result = spanish
                for i, group in enumerate(match.groups(), 1):
                    result = result.replace('{min_length}', group).replace('{max_length}', group)
                    result = result.replace('{pk_value}', group)
                return result

    return message


def translate_field_name(field_name: str) -> str:
    """
    Translate a field name from English to Spanish.

    Args:
        field_name: The field name in English.

    Returns:
        The translated field name in Spanish, or the original if not found.
    """
    return FIELD_TRANSLATIONS.get(field_name, field_name)


def translate_errors(errors: dict) -> dict:
    """
    Recursively translate all error messages and field names.

    Args:
        errors: Dictionary of error messages from DRF.

    Returns:
        Translated error dictionary with Spanish messages and field names.
    """
    translated = {}

    for field, messages in errors.items():
        translated_field = translate_field_name(field)

        if isinstance(messages, list):
            translated[translated_field] = [
                translate_error_message(str(msg)) for msg in messages
            ]
        elif isinstance(messages, dict):
            translated[translated_field] = translate_errors(messages)
        else:
            translated[translated_field] = translate_error_message(str(messages))

    return translated


def custom_exception_handler(exc, context):
    """
    Custom exception handler that translates error messages to Spanish.

    Args:
        exc: The exception that was raised.
        context: Additional context about the request.

    Returns:
        Response with translated error messages, or None if not handled.
    """
    # Call the default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        # Translate the error data
        if isinstance(response.data, dict):
            response.data = translate_errors(response.data)
        elif isinstance(response.data, list):
            response.data = [translate_error_message(str(msg)) for msg in response.data]
        elif isinstance(response.data, str):
            response.data = translate_error_message(response.data)

    return response
