from django.contrib import admin

from .models import Function, MathematicalObject, Modification, Name, Tag

admin.site.register(Function)
admin.site.register(MathematicalObject)
admin.site.register(Modification)
admin.site.register(Name)
admin.site.register(Tag)
