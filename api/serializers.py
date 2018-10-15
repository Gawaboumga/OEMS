from django.contrib.auth.models import User, Group
from django.core.files.base import ContentFile
from rest_framework import serializers

from api.models import Function, MathematicalObject, Name
from api.model_config import *


class FunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Function
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.function = validated_data.get('function', instance.function)
        return instance


class NameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Name
        fields = '__all__'


class FunctionMathematicalObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Function
        fields = ('function', )
        depth = 1


class NameMathematicalObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Name
        fields = ('name', )
        depth = 1


class MathematicalObjectSerializer(serializers.ModelSerializer):
    functions = FunctionMathematicalObjectSerializer(many=True, required=False)
    names = NameMathematicalObjectSerializer(many=True, required=False)
    description = serializers.CharField(required=False)

    class Meta:
        model = MathematicalObject
        fields = '__all__'
        extra_kwargs = {
            'related': {'required': False},
            'functions': {'required': False},
            'names': {'required': False},
            }

    def create(self, validated_data):
        related = validated_data.pop('related', [])
        functions = validated_data.pop('functions', [])
        names = validated_data.pop('names', [])
        description = validated_data.pop('description', None)
        mathematical_object = MathematicalObject.objects.create(**validated_data)
        for function in functions:
            mathematical_object.functions.create(**function)
        for name in names:
            mathematical_object.names.create(**name)
        for relation in related:
            mathematical_instance = MathematicalObject.objects.get(pk=relation)
            mathematical_object.related.add(mathematical_instance)
        if description:
            description_file = ContentFile(description)
            mathematical_object.description.save(str(mathematical_object.pk), description_file, save=True)
        mathematical_object.save()
        return mathematical_object

    def update(self, instance, validated_data):
        instance.latex = validated_data.get('latex', instance.latex)
        instance.type = validated_data.get('type', instance.type)
        return instance

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['description'] = instance.get_content()
        return ret


class MathematicalObjectIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = MathematicalObject
        fields = ('id', )
        extra_kwargs = {
            'id': {'read_only': False},
        }


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
