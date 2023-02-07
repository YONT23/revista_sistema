from ...serializers.persons.personSerializers import PersonsSerializers
from ....models import Persons
from django.http import Http404
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.response import Response
from .....helpers.createResponse import create_response
from rest_framework import status


class PersonView(ListAPIView):
    queryset = Persons.objects.all()
    serializer_class = PersonsSerializers

    def get(self, request, *args, **kwargs):
        data = self.get_queryset()
        serializers = PersonsSerializers(data, many=True)
        response, code = create_response(
            status.HTTP_200_OK, serializers.data)
        return Response(response, status=code)


class PersonCreateView(CreateAPIView):
    queryset = Persons.objects.all()
    serializer_class = PersonsSerializers

    def post(self, request, *args, **kwargs):
        personSerializers = PersonsSerializers(data=request.data)
        if personSerializers.is_valid():
            personSerializers.save()
            response, code = create_response(
                status.HTTP_200_OK, personSerializers.data)
            return Response(response, status=code)
        response, code = create_response(
            status.HTTP_400_BAD_REQUEST, personSerializers.data)
        return Response(response, status=code)


class PersonUpdateView(UpdateAPIView):
    queryset = Persons.objects.all()
    serializer_class = PersonsSerializers

    def get_object(self):
        try:
            pk = self.request.user.id
            return Persons.objects.filter(user__id=pk)[0]
        except Persons.DoesNotExist:
            response, code = create_response(
                status.HTTP_200_OK, 'No Found')
            raise Response(response, status=code)

    def put(self, request, *args, **kwargs):
        person = self.get_object()
        personSerializers = PersonsSerializers(person, data=request.data)
        if personSerializers.is_valid():
            personSerializers.update()
            response, code = create_response(
                status.HTTP_200_OK, personSerializers.data)
            return Response(response, status=code)
        response, code = create_response(
            status.HTTP_200_OK, personSerializers.data)
        return Response(response, status=code)
