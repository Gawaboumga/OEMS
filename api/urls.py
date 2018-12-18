from django.urls import path
from django.conf import settings
from api.LatexFinder import LatexFinder
import logging
import os
from api import ajax, models, views

app_name = 'api'

urlpatterns = [
    path('objects/', views.MathematicalObjectList.as_view(), name="mathematical_objects"),
    path('objects/<int:pk>/', views.MathematicalObjectDetail.as_view(), name="mathematical_object"),
    path('functions/', views.FunctionList.as_view(), name="functions"),
    path('functions/<int:pk>/', views.FunctionDetail.as_view(), name="function"),
    path('names/', views.NameList.as_view(), name="names"),
    path('names/<int:pk>/', views.NameDetail.as_view(), name="name"),
    path('tags/', views.TagList.as_view(), name="tags"),
    path('tags/<int:pk>/', views.TagDetail.as_view(), name="tag"),
    path('objects/<int:object_pk>/functions/', views.MathematicalObjectFunctionList.as_view(), name="mathematical_object_functions"),
    path('objects/<int:object_pk>/functions/<int:function_pk>', views.MathematicalObjectFunctionDetail.as_view(), name="mathematical_object_function"),
    path('objects/<int:object_pk>/names/', views.MathematicalObjectNameList.as_view(), name="mathematical_object_names"),
    path('objects/<int:object_pk>/names/<int:name_pk>', views.MathematicalObjectNameDetail.as_view(), name="mathematical_object_name"),
    path('objects/<int:object_pk>/related/', views.MathematicalObjectRelatedList.as_view(), name="mathematical_object_relations"),
    path('objects/<int:object_pk>/related/<int:other_pk>', views.MathematicalObjectRelatedDetail.as_view(), name="mathematical_object_relation"),
    path('objects/<int:object_pk>/tags/', views.MathematicalObjectTagList.as_view(), name="mathematical_object_tags"),
    path('objects/<int:object_pk>/tags/<int:tag_pk>', views.MathematicalObjectTagDetail.as_view(), name="mathematical_object_tag"),

    path('function-autocomplete/', ajax.FunctionAutocomplete.as_view(
        model=models.Function,
        create_field='function',
    ), name='function-autocomplete'),
    path('name-autocomplete/', ajax.NameAutocomplete.as_view(
        model=models.Name,
        create_field='name',
    ), name='name-autocomplete'),
    path('tag-autocomplete/', ajax.TagAutocomplete.as_view(
        model=models.Tag,
        create_field='tag',
    ), name='tag-autocomplete'),
]


def check_consistency(logger, objects, field, folder):
    existing = set()
    pointed = set()
    missing = []

    for object in objects:
        if field(object):
            path = field(object).name
            if os.path.isfile(path):
                pointed.add(path)
            else:
                missing.append(path)

    path = os.path.join(settings.MEDIA_ROOT, folder)
    for file in os.listdir(path):
        existing.add(os.path.join(settings.MEDIA_ROOT, folder, file))

    for m in missing:
        logger.error(f"Missing file: {m}")

    for m in existing.difference(pointed):
        logger.error(f"Existing file: {m} but not pointed by any")

    for m in pointed.difference(existing):
        logger.error(f"Pointed file: {m} but not existing")


def check_consistency_mathematical_objects(logger):
    check_consistency(logger, models.MathematicalObject.objects.all(), lambda x: x.description, 'mathematical_objects/')


def check_consistency_modifications(logger):
    check_consistency(logger, models.Modification.objects.all(), lambda x: x.new_description, 'modifications/')


def create_query_latex(logger):
    latex_finder = LatexFinder()
    for mathematical_object in models.MathematicalObject.objects.all():
        latex_finder.add(mathematical_object.pk, mathematical_object.latex)
    return latex_finder


def one_time_startup():
    logger = logging.getLogger(__name__)

    check_consistency_mathematical_objects(logger)
    check_consistency_modifications(logger)

    create_query_latex(logger)




one_time_startup()
