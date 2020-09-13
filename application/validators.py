from marshmallow import fields, validate, ValidationError


def validate_len(input_field, length):
    if len(input_field.strip()) < length:
        raise ValidationError(
            'Field must not be less than {} characters long'.format(length)
        )
