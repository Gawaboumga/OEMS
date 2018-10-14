from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from api.LatexFinder import LatexFinder


def validate_latex(value: str):
    exception_message = None
    try:
        LatexFinder().is_valid(value)
        return
    except Exception as e:
        exception_message = str(e)

    tokens = exception_message.split('expecting')
    if tokens:
        raise ValidationError(
            _(tokens[0])
        )
    else:
        raise ValidationError(
            _("Invalid input")
        )
