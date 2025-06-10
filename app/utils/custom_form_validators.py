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

def validate_date_range(form, field):
    start_date = form.start_date.data
    end_date = field.data

    if end_date and start_date:
        if end_date.date() < start_date.date():
            raise ValidationError('End date must be the same or after the start date.')

        if end_date.date() == start_date.date():
            if end_date.time() < start_date.time():
                raise ValidationError('End time must be after start time for same-day tours.')

def message_length_check(form, field):
    length = len(field.data or '')

    if length < 30:
        raise ValidationError('Message is too short. Minimum 30 characters required.')

    if length > 500:
        raise ValidationError('Message is too long. Maximum 500 characters allowed.')
