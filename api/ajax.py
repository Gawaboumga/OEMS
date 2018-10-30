from dal import autocomplete

from api.models import Function, Name, Tag


class FunctionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Function.objects.none().order_by('pk')

        qs = Function.objects.all()

        if self.q:
            qs = qs.filter(function__istartswith=self.q)

        return qs.order_by('pk')


class NameAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Name.objects.none().order_by('name')

        qs = Name.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs.order_by('name')


class TagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Tag.objects.none().order_by('tag')

        qs = Tag.objects.all()
        if self.q:
            qs = qs.filter(tag__istartswith=self.q)

        return qs.order_by('tag')
