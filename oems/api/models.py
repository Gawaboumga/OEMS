from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
import os

from api.model_config import *


class Function(models.Model):
    id = models.AutoField(primary_key=True)
    function = models.CharField(max_length=FUNCTION_REPRESENTATION_MAX_LENGTH)

    def __str__(self):
        return self.function


class Name(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=NAME_REPRESENTATION_MAX_LENGTH)

    def __str__(self):
        return self.name


class MathematicalObject(models.Model):
    id = models.AutoField(primary_key=True)
    latex = models.CharField(max_length=MATHEMATICAL_OBJECT_REPRESENTATION_MAX_LENGTH)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    related = models.ManyToManyField('self')
    functions = models.ManyToManyField(Function)
    names = models.ManyToManyField(Name)
    description = models.FileField(upload_to='mathematical_objects/', blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def get_content(self):
        content = ''
        if self.description:
            with self.description.open(mode='r') as f:
                content = f.read()
        return content

    def save_content(self, content):
        if self.description:
            with self.description.open(mode='w') as f:
                f.write(content)
        else:
            new_description_file = ContentFile(content)
            self.description.save(str(self.pk), new_description_file, save=True)

    def __str__(self):
        return str(self.id) + ' > ' + self.latex


class Modification(models.Model):
    mathematical_object = models.ForeignKey(MathematicalObject, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now=True)
    new_description = models.FileField(upload_to='modifications/')

    def get_content(self):
        content = ''
        if self.new_description:
            with self.new_description.open(mode='r') as f:
                content = f.read()
        return content


def _delete_file(path):
    # Deletes file from filesystem.
    if os.path.isfile(path):
        os.remove(path)


@receiver(post_delete, sender=MathematicalObject)
def delete_description_pre_delete_mathematical_object(sender, instance, *args, **kwargs):
    if instance.description:
        _delete_file(instance.description.path)


@receiver(post_delete, sender=Modification)
def delete_description_pre_delete_modification(sender, instance, *args, **kwargs):
    if instance.new_description:
        _delete_file(instance.new_description.path)
