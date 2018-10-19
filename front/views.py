from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic

from api import models, LatexFinder
from front import forms


PAGINATION_SIZE = 25


@login_required
@permission_required('api.add_mathematicalobject', raise_exception=True)
def create_mathematical_object(request):
    if request.method == 'POST':
        mathematical_object_form = forms.MathematicalObjectForm(request.POST)
        if mathematical_object_form.is_valid():
            new_instance = mathematical_object_form.save()
            return redirect('front:mathematical_object', pk=new_instance.pk)
    else:
        mathematical_object_form = forms.MathematicalObjectForm()
    return render(request, "front/mathematical_object_creation.html", {'form': mathematical_object_form})


@login_required
@permission_required('api.change_mathematicalobject', raise_exception=True)
def edit_mathematical_object(request, pk):
    mathematical_object_instance = get_object_or_404(models.MathematicalObject, pk=pk)
    if request.method == 'POST':
        mathematical_object_form = forms.MathematicalObjectForm(request.POST, initial={'description': mathematical_object_instance.get_content()}, instance=mathematical_object_instance)
        if mathematical_object_form.is_valid():
            instance = mathematical_object_form.save()
            return redirect('front:mathematical_object', pk=instance.pk)

    mathematical_object_form = forms.MathematicalObjectForm(initial={'description': mathematical_object_instance.get_content()}, instance=mathematical_object_instance)
    return render(request, "front/mathematical_object_creation.html", {'form': mathematical_object_form})


@login_required
def edit_mathematical_object_description(request, pk):
    mathematical_object_instance = get_object_or_404(models.MathematicalObject, pk=pk)
    if request.method == 'POST':
        modification_form = forms.ModificationForm(request.POST)
        if modification_form.is_valid():
            new_modification = modification_form.save(mathematical_object_instance, request.user)
            return redirect('front:modification', pk=new_modification.pk)
    else:
        modification_form = forms.ModificationForm(initial={
            'new_description': mathematical_object_instance.get_content()
        })
    return render(request, "front/mathematical_object_description_edition.html", {'form': modification_form})


def index(request):
    number_series = models.MathematicalObject.objects.count()
    form = forms.QueryForm()
    form.fields['q'].widget.attrs['placeholder'] = 'Type any series or product in LaTeX !'
    form.fields['q'].label = ''
    return render(request, "front/index.html", {'number_series': number_series, 'form': form})


class FunctionListView(generic.ListView):
    model = models.Function
    ordering = 'id'
    template_name = 'front/functions.html'
    paginate_by = PAGINATION_SIZE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = forms.QueryForm()
        form.fields['q'].widget.attrs['placeholder'] = 'Type any function !'
        form.fields['q'].label = ''
        context['form'] = form
        return context

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        if query:
            return super().get_queryset().filter(function__icontains=query)
        return super().get_queryset()


class FunctionDetailView(generic.DetailView):
    model = models.Function
    template_name = 'front/function.html'
    context_object_name = 'function'


class MathematicalObjectListView(generic.ListView):
    model = models.MathematicalObject
    ordering = 'id'
    template_name = 'front/mathematical_objects.html'
    context_object_name = 'mathematical_objects'
    paginate_by = PAGINATION_SIZE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = forms.QueryForm()
        form.fields['q'].widget.attrs['placeholder'] = 'Type any series or product in LaTeX !'
        form.fields['q'].label = ''
        context['form'] = form
        return context

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        if query:
            try:
                LatexFinder.LatexFinder().is_valid(query)
            except Exception:
                return super().get_queryset()

            results = LatexFinder.LatexFinder().search(query)
            results = list(map(lambda x: x[0], results))
            clauses = ' '.join(['WHEN id=%s THEN %s' % (pk, i) for i, pk in enumerate(results)])
            ordering = 'CASE %s END' % clauses
            queryset = super().get_queryset().filter(pk__in=results).extra(
                select={'ordering': ordering}, order_by=('ordering',))

            return queryset
        return super().get_queryset()


class MathematicalObjectDetailView(generic.DetailView):
    model = models.MathematicalObject
    template_name = 'front/mathematical_object.html'
    context_object_name = 'mathematical_object'


class ModificationListView(PermissionRequiredMixin, generic.ListView):
    model = models.Modification
    ordering = 'date_created'
    template_name = 'front/modifications.html'
    context_object_name = 'modifications'
    permission_required = ('api.delete_modification',)
    paginate_by = PAGINATION_SIZE


@login_required
def modification_detail(request, pk):
    modification = get_object_or_404(models.Modification, pk=pk)

    if not (request.user.has_perm('api.delete_proposition') or request.user == modification.user):
        return HttpResponseForbidden()

    if request.method == "POST":
        if request.POST.get('accept_modification'):
            if not request.user.has_perm('api.delete_proposition'):
                return HttpResponseForbidden()

            accepted_modification = modification
            mathematical_object = accepted_modification.mathematical_object
            mathematical_object.save_content(accepted_modification.get_content())
            accepted_modification.new_description.delete()
            accepted_modification.delete()
            return redirect('front:mathematical_object', pk=mathematical_object.pk)
        elif request.POST.get('reject_modification'):
            rejected_modification = modification
            rejected_modification.new_description.delete()
            rejected_modification.delete()
            if request.user.has_perm('api.delete_proposition'):
                return redirect('front:modifications')
            else:
                return redirect('front:mathematical_object', pk=modification.mathematical_object.pk)
    else:
        return render(request, 'front/modification.html', {'modification': modification})


class NameListView(generic.ListView):
    model = models.Name
    ordering = 'name'
    template_name = 'front/names.html'
    context_object_name = 'names'
    paginate_by = PAGINATION_SIZE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = forms.QueryForm()
        form.fields['q'].widget.attrs['placeholder'] = 'Type a name !'
        form.fields['q'].label = ''
        context['form'] = form
        return context

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        if query:
            return super().get_queryset().filter(name__icontains=query)
        return super().get_queryset()


class NameDetailView(generic.DetailView):
    model = models.Name
    template_name = 'front/name.html'
    context_object_name = 'name'


class TagListView(generic.ListView):
    model = models.Tag
    ordering = 'tag'
    template_name = 'front/tags.html'
    context_object_name = 'tags'
    paginate_by = PAGINATION_SIZE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = forms.QueryForm()
        form.fields['q'].widget.attrs['placeholder'] = 'Type a tag !'
        form.fields['q'].label = ''
        context['form'] = form
        return context

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        if query:
            return super().get_queryset().filter(tag__icontains=query)
        return super().get_queryset()


class TagDetailView(generic.DetailView):
    model = models.Tag
    template_name = 'front/tag.html'
    context_object_name = 'tag'


class PropositionListView(PermissionRequiredMixin, generic.ListView):
    model = models.Proposition
    ordering = 'date_created'
    template_name = 'front/propositions.html'
    context_object_name = 'propositions'
    permission_required = ('api.delete_proposition', )
    paginate_by = PAGINATION_SIZE


@login_required
def create_proposition(request):
    if request.method == 'POST':
        form = forms.PropositionForm(request.POST)
        if form.is_valid():
            proposition = form.save(commit=False)
            proposition.user = request.user
            proposition.save()
            return redirect('front:proposition', pk=proposition.pk)
    else:
        form = forms.PropositionForm()

    return render(request, 'front/proposition_creation.html', {'form': form})


@login_required
def proposition_detail(request, pk):
    proposition = get_object_or_404(models.Proposition, pk=pk)

    if not (request.user.has_perm('api.delete_proposition') or request.user == proposition.user):
        return HttpResponseForbidden()

    if request.method == "POST":
        proposition.delete()
        if request.user.has_perm('api.delete_proposition'):
            return redirect('front:propositions')
        else:
            return redirect('front:index')
    else:
        return render(request, 'front/proposition.html', {'proposition': proposition})
