from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_NIN_digits(value):
    if not value.isnumeric():
        raise ValidationError(
            _("%(value)s is not a valid NIN"),
            params={"value": value},
        )
