def validate_email(email):
    from django.core.validators import validate_email as validate
    from django.core.exceptions import ValidationError
    try:
        validate(email)
        return True
    except ValidationError:
        return False
