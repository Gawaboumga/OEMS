from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from api.models import Function, Name, MathematicalObject
from api.serializers import FunctionSerializer, NameSerializer, MathematicalObjectSerializer, MathematicalObjectIdSerializer, UserSerializer, GroupSerializer
from rest_framework import generics, mixins, status, viewsets
from rest_framework.response import Response


class FunctionList(generics.ListCreateAPIView):
    """
    List all functions, or create a new function.
    """
    queryset = Function.objects.all()
    serializer_class = FunctionSerializer


class FunctionDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    """
    Retrieve, update or delete a function instance.
    """
    queryset = Function.objects.all()
    serializer_class = FunctionSerializer

    def get(self, request, pk, format=None):
        function_object = get_object_or_404(Function, pk=pk)
        results = MathematicalObject.objects.filter(functions=function_object)
        serializer = MathematicalObjectIdSerializer(results, many=True)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        function_object = get_object_or_404(Function, pk=pk)
        serializer = FunctionSerializer(function_object, data=request.data)
        if serializer.is_valid():
            new_function = serializer.save()
            new_function.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        function_object = get_object_or_404(Function, pk=pk)
        function_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NameList(generics.ListCreateAPIView):
    """
    List all names, or create a new name.
    """
    queryset = Name.objects.all()
    serializer_class = NameSerializer


class NameDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    """
    Retrieve, update or delete a name instance.
    """
    queryset = Name.objects.all()
    serializer_class = NameSerializer

    def get(self, request, pk, format=None):
        name_object = get_object_or_404(Name, pk=pk)
        results = MathematicalObject.objects.filter(names=name_object)
        serializer = MathematicalObjectIdSerializer(results, many=True)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        name_object = get_object_or_404(Name, pk=pk)
        serializer = NameSerializer(name_object, data=request.data)
        if serializer.is_valid():
            new_name = serializer.save()
            new_name.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        name_object = get_object_or_404(Name, pk=pk)
        name_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MathematicalObjectList(generics.ListCreateAPIView):
    """
    List all mathematical objects, or create a new mathematical object.
    """
    queryset = MathematicalObject.objects.all()
    serializer_class = MathematicalObjectSerializer


class MathematicalObjectDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a mathematical object instance.
    """
    queryset = MathematicalObject.objects.all()
    serializer_class = MathematicalObjectSerializer


class MathematicalObjectFunctionList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    """
    List all functions liked to a mathematical object, or add a new function to a mathematical object.
    """
    queryset = Function.objects.all()
    serializer_class = FunctionSerializer

    def get(self, request, object_pk, format=None):
        mathematical_object = get_object_or_404(MathematicalObject, pk=object_pk)
        serializer = FunctionSerializer(mathematical_object.functions, many=True)
        return Response(serializer.data)

    def post(self, request, object_pk, format=None):
        mathematical_object = get_object_or_404(MathematicalObject, pk=object_pk)
        serializer = FunctionSerializer(data=request.data)
        if serializer.is_valid():
            mathematical_object.functions.add(serializer.save())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MathematicalObjectFunctionDetail(mixins.DestroyModelMixin, generics.GenericAPIView):
    """
    Retrieve, update or delete a function linked to mathematical objects.
    """
    queryset = Function.objects.all()
    serializer_class = FunctionSerializer

    def delete(self, request, object_pk, function_pk, format=None):
        mathematical_object = get_object_or_404(MathematicalObject, pk=object_pk)
        function_object = get_object_or_404(Function, pk=function_pk)
        mathematical_object.functions.remove(function_object)
        if Function.objects.filter(mathematicalobject=mathematical_object).count() == 0:
            function_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MathematicalObjectNameList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    """
    List all names liked to a mathematical object, or add a new name to a mathematical object.
    """
    queryset = Name.objects.all()
    serializer_class = NameSerializer

    def get(self, request, object_pk, format=None):
        mathematical_object = get_object_or_404(MathematicalObject, pk=object_pk)
        serializer = NameSerializer(mathematical_object.names, many=True)
        return Response(serializer.data)

    def post(self, request, object_pk, format=None):
        mathematical_object = get_object_or_404(MathematicalObject, pk=object_pk)
        serializer = NameSerializer(data=request.data)
        if serializer.is_valid():
            mathematical_object.names.add(serializer.save())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MathematicalObjectNameDetail(mixins.DestroyModelMixin, generics.GenericAPIView):
    """
    Retrieve, update or delete a name linked to mathematical objects.
    """
    queryset = Name.objects.all()
    serializer_class = NameSerializer

    def delete(self, request, object_pk, name_pk, format=None):
        mathematical_object = get_object_or_404(MathematicalObject, pk=object_pk)
        name_object = get_object_or_404(Name, pk=name_pk)
        mathematical_object.names.remove(name_object)
        if Name.objects.filter(mathematicalobject=mathematical_object).count() == 0:
            name_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MathematicalObjectRelatedList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    """
    List all related to a mathematical object, or add a new relation to a mathematical object.
    """
    queryset = MathematicalObject.objects.all()
    serializer_class = MathematicalObjectIdSerializer

    def get(self, request, object_pk, format=None):
        mathematical_object = get_object_or_404(MathematicalObject, pk=object_pk)
        serializer = MathematicalObjectIdSerializer(mathematical_object.related, many=True)
        return Response(serializer.data)

    def post(self, request, object_pk, format=None):
        mathematical_object = get_object_or_404(MathematicalObject, pk=object_pk)
        serializer = MathematicalObjectIdSerializer(data=request.data)
        if serializer.is_valid():
            other_mathematical_object = get_object_or_404(MathematicalObject, pk=serializer.validated_data['id'])
            mathematical_object.related.add(other_mathematical_object)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MathematicalObjectRelatedDetail(mixins.DestroyModelMixin, generics.GenericAPIView):
    """
    Retrieve, update or delete a relation between mathematical objects.
    """
    queryset = MathematicalObject.objects.all()
    serializer_class = MathematicalObjectIdSerializer

    def delete(self, request, object_pk, other_pk, format=None):
        mathematical_object = get_object_or_404(MathematicalObject, pk=object_pk)
        other_mathematical_object = get_object_or_404(MathematicalObject, pk=other_pk)
        mathematical_object.related.remove(other_mathematical_object)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


