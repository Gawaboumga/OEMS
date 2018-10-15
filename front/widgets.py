
from django.forms.widgets import TextInput


class LatexInput(TextInput):
    input_type = 'text'
    template_name = 'forms/widgets/latex.html'
