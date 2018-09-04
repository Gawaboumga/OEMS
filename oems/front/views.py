from django.shortcuts import render

from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required

from api import models
from front import forms
from django.shortcuts import get_object_or_404, redirect, HttpResponseRedirect


PAGINATION_SIZE = 25


def create_mathematical_object(request):
    if request.method == 'POST':
        mathematical_object_form = forms.MathematicalObjectForm(request.POST)
        if mathematical_object_form.is_valid():
            new_instance = mathematical_object_form.save()
            return redirect('front:mathematical_object', pk=new_instance.pk)
    else:
        mathematical_object_form = forms.MathematicalObjectForm()
    return render(request, "front/mathematical_object_creation.html", {'form': mathematical_object_form})


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
    return render(request, "front/index.html", {'number_series': number_series})


class FunctionListView(generic.ListView):
    model = models.Function
    ordering = 'id'
    template_name = 'front/functions.html'
    paginate_by = PAGINATION_SIZE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.QueryForm()
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
        context['form'] = forms.QueryForm()
        return context

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        if query:
            return super().get_queryset().filter(latex__icontains=query)
        return super().get_queryset()


class MathematicalObjectDetailView(generic.DetailView):
    model = models.MathematicalObject
    template_name = 'front/mathematical_object.html'
    context_object_name = 'mathematical_object'


class ModificationListView(generic.ListView):
    model = models.Modification
    ordering = 'date_created'
    template_name = 'front/modifications.html'
    context_object_name = 'modifications'
    paginate_by = PAGINATION_SIZE


class ModificationDetailView(generic.DetailView):
    model = models.Modification
    template_name = 'front/modification.html'
    context_object_name = 'modification'

    def post(self, request, *args, **kwargs):
        if request.POST.get('accept_modification'):
            accepted_modification = self.get_object()
            mathematical_object = accepted_modification.mathematical_object
            mathematical_object.save_content(accepted_modification.get_content())
            accepted_modification.new_description.delete()
            accepted_modification.delete()
            return redirect('front:mathematical_object', pk=mathematical_object.pk)
        elif request.POST.get('reject_modification'):
            rejected_modification = self.get_object()
            rejected_modification.new_description.delete()
            rejected_modification.delete()
            return redirect('front:modifications')

        return self.get(request, args, kwargs)


class NameListView(generic.ListView):
    model = models.Name
    ordering = 'name'
    template_name = 'front/names.html'
    context_object_name = 'names'
    paginate_by = PAGINATION_SIZE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.QueryForm()
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
