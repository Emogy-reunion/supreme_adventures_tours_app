from wtforms.validators import ValidationError

def custom_length_check(form, field):
    length = len(field.data or '')

    if length < 150:
        raise ValidationError('Description is too short. Minimum 150 characters required.')

    if length > 1500:
        raise ValidationError('Description is too long. Maximum 1500 characters allowed.')

def validate_price_range(form, field):
    minimum_price = form.minimum_price.data
    maximum_price = field.data


    if minimum_price is not None and maximum_price is not None and maximum_price < minimum_price:
        raise ValidationError("Maximum price must be greater than or equal to minimum price.")

