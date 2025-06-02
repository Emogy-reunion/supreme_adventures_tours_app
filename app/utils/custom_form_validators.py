def custom_length_check(form, field):
    length = len(field.data or '')

    if length < 150:
        raise ValidationError('Description is too short. Minimum 150 characters required.')

    if length > 1500:
        raise ValidationError('Description is too long. Maximum 1500 characters allowed.')
