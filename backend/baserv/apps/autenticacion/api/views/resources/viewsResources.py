from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from ...permission.IsAdmin import IsAdminRole
from .....helpers.createResponse import create_response
from ....models import Resources
from ...serializers.resources.resourceSerializer import ResourcesSerializers


class ResourcesListView(ListAPIView):
    queryset = Resources.objects.all()
    serializer_class = ResourcesSerializers

    def get(self, request, *args, **kwargs):
        data = self.get_queryset()
        serializers = ResourcesSerializers(data, many=True)
        response, code = create_response(
            status.HTTP_200_OK, 'Resources', serializers.data)
        return Response(response, status=code)

class ResourcesUpdateView(UpdateAPIView):
    queryset = Resources.objects.all()
    serializer_class = ResourcesSerializers

    def get_object(self):
        try:
            pk = self.kwargs.get('pk')
            return Resources.objects.get(pk=pk)
        except Resources.DoesNotExist:
            response, code = create_response(
                status.HTTP_400_BAD_REQUEST, 'Not Found')
            return {'response': response, 'code': code}

    def path(self, request, *args, **kwargs):
        resources = self.get_object()
        if type(resources) is dict:
            return Response(resources['response'], resources['code'])
        resourcesSerializers = ResourcesSerializers(
            resources, data=request.data)
        if resourcesSerializers.is_valid():
            resourcesSerializers.save()
            response, code = create_response(
                status.HTTP_200_OK, 'Resources Update', resourcesSerializers.data)
            return Response(response, status=code)
        response, code = create_response(
            status.HTTP_400_BAD_REQUEST, 'Error', resourcesSerializers.errors)
        return Response(response, status=code)


class ResourcesDestroyView(DestroyAPIView):
    queryset = Resources.objects.all()
    serializer_class = ResourcesSerializers
    permission_classes = [IsAdminRole]

    def get_object(self):
        try:
            pk = self.kwargs.get('pk')
            return Resources.objects.get(id=pk)
        except Resources.DoesNotExist:
            return None

    def delete(self, request, *args, **kwargs):
        resources = self.get_object()
        if resources is None:
            response, code = create_response(
                status.HTTP_200_OK, 'Error', 'Resources Not Exist')
            return Response(response, status=code)
        resources.delete()

        response, code = create_response(
            status.HTTP_200_OK, 'Error', 'Ok')
        return Response(response, status=code)
