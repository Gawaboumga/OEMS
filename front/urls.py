from django.urls import path

from . import views

app_name = 'front'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('functions/', views.FunctionListView.as_view(), name='functions'),
    path('functions/<int:pk>', views.FunctionDetailView.as_view(), name='function'),
    path('names/', views.NameListView.as_view(), name='names'),
    path('names/<int:pk>', views.NameDetailView.as_view(), name='name'),
    path('modifications/', views.ModificationListView.as_view(), name='modifications'),
    path('modifications/<int:pk>', views.modification_detail, name='modification'),
    path('object_creation/', views.create_mathematical_object, name='mathematical_object_creation'),
    path('object_edition/<int:pk>/', views.edit_mathematical_object, name='mathematical_object_edition'),
    path('objects/<int:pk>/description/', views.edit_mathematical_object_description, name='mathematical_object_description_edition'),
    path('objects/', views.MathematicalObjectListView.as_view(), name='mathematical_objects'),
    path('objects/<int:pk>/', views.MathematicalObjectDetailView.as_view(), name='mathematical_object'),
    path('propositions/', views.PropositionListView.as_view(), name='propositions'),
    path('proposition_creation/', views.create_proposition, name='proposition_creation'),
    path('proposition/<int:pk>/', views.proposition_detail, name='proposition'),
    path('tags/', views.TagListView.as_view(), name='tags'),
    path('tags/<int:pk>', views.TagDetailView.as_view(), name='tag'),
]
