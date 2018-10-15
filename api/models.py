from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.db.models.signals import post_delete, post_init, post_save
from django.dispatch.dispatcher import receiver
import logging
import os

from api.LatexFinder import LatexFinder
from api.model_config import *


def _delete_file(path):
    # Deletes file from filesystem.
    if os.path.isfile(path):
        os.remove(path)


class Function(models.Model):
    function = models.CharField(max_length=FUNCTION_REPRESENTATION_MAX_LENGTH)

    def __str__(self):
        return self.function


class Name(models.Model):
    name = models.CharField(max_length=NAME_REPRESENTATION_MAX_LENGTH)

    def __str__(self):
        return self.name


class MathematicalObject(models.Model):
    latex = models.CharField(max_length=MATHEMATICAL_OBJECT_REPRESENTATION_MAX_LENGTH)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    related = models.ManyToManyField('self')
    functions = models.ManyToManyField(Function)
    names = models.ManyToManyField(Name)
    description = models.FileField(upload_to='mathematical_objects/', blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def get_content(self):
        if not self.description:
            return ''

        try:
            with self.description.open(mode='r') as f:
                return f.read()
        except FileNotFoundError as e:
            logging.fatal('Mathematical object file not found for object: {}'.format(self.pk), exc_info=True)
            raise e

    def save_content(self, content):
        if self.description:
            with self.description.open(mode='w') as f:
                f.write(content)
        else:
            new_description_file = ContentFile(content)
            self.description.save(str(self.pk), new_description_file, save=True)

    def __str__(self):
        return str(self.id) + ' > ' + self.latex


@receiver(post_init, sender=MathematicalObject)
def remember_state(sender, **kwargs):
    instance = kwargs.get('instance')
    instance.previous_latex = instance.latex


@receiver(post_save, sender=MathematicalObject)
def update_latex_query(sender, **kwargs):
    instance = kwargs.get('instance')
    created = kwargs.get('created')
    if instance.previous_latex != instance.latex or created:
        latex_finder = LatexFinder()
        if not created:
            latex_finder.remove(instance.pk)
        latex_finder.add(instance.pk, instance.latex)


@receiver(post_delete, sender=MathematicalObject)
def delete_description_pre_delete_mathematical_object(sender, instance, *args, **kwargs):
    latex_finder = LatexFinder()
    latex_finder.remove(instance.pk)

    if instance.description:
        _delete_file(instance.description.path)


class Modification(models.Model):
    mathematical_object = models.ForeignKey(MathematicalObject, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now=True)
    new_description = models.FileField(upload_to='modifications/')

    def get_content(self):
        if not self.new_description:
            return ''

        try:
            with self.new_description.open(mode='r') as f:
                return f.read()
        except FileNotFoundError as e:
            logging.fatal('Modification file not found for object: {}'.format(self.pk), exc_info=True)
            raise e


class Proposition(models.Model):
    content = models.TextField(max_length=PROPOSITION_REPRESENTATION_MAX_LENGTH)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now=True)


@receiver(post_delete, sender=Modification)
def delete_description_pre_delete_modification(sender, instance, *args, **kwargs):
    if instance.new_description:
        _delete_file(instance.new_description.path)
