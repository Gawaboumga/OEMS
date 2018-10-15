from dal import autocomplete

from api.models import Function, Name


class FunctionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Function.objects.none()

        qs = Function.objects.all()

        if self.q:
            qs = qs.filter(function__istartswith=self.q)

        return qs


class NameAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Name.objects.none()

        qs = Name.objects.all().order_by('name')

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
