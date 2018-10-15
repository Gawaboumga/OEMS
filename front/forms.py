from django import forms
from django.core.files.base import ContentFile

from api import models, validators
from front import widgets
from dal import autocomplete
from pagedown.widgets import PagedownWidget


class QueryForm(forms.Form):
    q = forms.CharField(required=False)


class MathematicalObjectForm(forms.ModelForm):
    description = forms.CharField(required=False, widget=PagedownWidget(attrs={'onkeyup': 'MathJax.Hub.Queue(["Typeset", MathJax.Hub])'}))

    class Meta:
        model = models.MathematicalObject
        fields = '__all__'

        widgets = {
            'latex': widgets.LatexInput(),
            'functions': autocomplete.ModelSelect2Multiple(url='api:function-autocomplete'),
            'names': autocomplete.ModelSelect2Multiple(url='api:name-autocomplete')
        }

    def __init__(self, *args, **kwargs):
        super(MathematicalObjectForm, self).__init__(*args, **kwargs)
        self.fields['related'].required = False
        self.fields['functions'].required = False
        self.fields['names'].required = False

    def clean(self):
        super().clean()
        validators.validate_latex(self.cleaned_data.get('latex'))

    def save(self):
        super().save()
        description = self.cleaned_data['description']
        if description:
            description_file = ContentFile(description)
            self.instance.description.save(str(self.instance.pk), description_file, save=True)
        return self.instance


class ModificationForm(forms.Form):
    new_description = forms.CharField(required=True, widget=PagedownWidget(attrs={'onkeyup': 'MathJax.Hub.Queue(["Typeset", MathJax.Hub])'}))

    def save(self, mathematical_object, user):
        new_description_instance = models.Modification.objects.create(
            mathematical_object=mathematical_object,
            user=user
        )

        new_description = self.cleaned_data['new_description']
        if new_description:
            new_description_file = ContentFile(new_description)
            new_description_instance.new_description.save(str(new_description_instance.pk), new_description_file, save=True)
        return new_description_instance


class PropositionForm(forms.ModelForm):
    class Meta:
        model = models.Proposition
        fields = ('content', )
