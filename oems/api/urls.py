from django.urls import path

from api import ajax, views

app_name = 'api'

urlpatterns = [
    path('objects/', views.MathematicalObjectList.as_view(), name="mathematical_objects"),
    path('objects/<int:pk>/', views.MathematicalObjectDetail.as_view(), name="mathematical_object"),
    path('functions/', views.FunctionList.as_view(), name="functions"),
    path('functions/<int:pk>/', views.FunctionDetail.as_view(), name="function"),
    path('names/', views.NameList.as_view(), name="names"),
    path('names/<int:pk>/', views.NameDetail.as_view(), name="name"),
    path('objects/<int:object_pk>/functions/', views.MathematicalObjectFunctionList.as_view(), name="mathematical_object_functions"),
    path('objects/<int:object_pk>/functions/<int:function_pk>', views.MathematicalObjectFunctionDetail.as_view(), name="mathematical_object_function"),
    path('objects/<int:object_pk>/names/', views.MathematicalObjectNameList.as_view(), name="mathematical_object_names"),
    path('objects/<int:object_pk>/names/<int:name_pk>', views.MathematicalObjectNameDetail.as_view(), name="mathematical_object_name"),
    path('objects/<int:object_pk>/related/', views.MathematicalObjectRelatedList.as_view(), name="mathematical_object_relations"),
    path('objects/<int:object_pk>/related/<int:other_pk>', views.MathematicalObjectRelatedDetail.as_view(), name="mathematical_object_relation"),

    path('function-autocomplete/', ajax.FunctionAutocomplete.as_view(), name='function-autocomplete'),
    path('name-autocomplete/', ajax.NameAutocomplete.as_view(), name='name-autocomplete'),
]
