from django.urls import path
from django.conf import settings
from api.LatexFinder import LatexFinder
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


def one_time_startup():
    query_file_name = 'db'
    path = os.path.join(settings.MEDIA_ROOT, 'latex_query', query_file_name)
    latex_finder = LatexFinder()
    latex_finder.load(path)


one_time_startup()
