from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework import status
from ...serializers.users.userSerializers import UserSerializers, CreateUserSerializers, UserChangePassword
from ....models import Users
from .....helpers.createResponse import create_response


class UsersView(RetrieveAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializers

    def get_object(self):
        try:
            request_user = self.request.user.id
            user = Users.objects.get(pk=request_user)
            return user
        except Users.DoesNotExist:
            return None
        except Exception as e:
            return None

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            users = self.get_queryset()
            serializers = UserSerializers(
                users, context={'request': request}, many=True)
            response, code = create_response(
                status.HTTP_200_OK, 'User', serializers.data)
            return Response(response, status=code)

        data = self.get_object()

        if data is None:
            response, code = create_response(
                status.HTTP_400_BAD_REQUEST, 'User', 'User Not found')
            return Response(response, status=code)

        try:
            serializers = UserSerializers(data)
            response, code = create_response(
                status.HTTP_200_OK, 'User', serializers.data)
            return Response(response, status=code)
        except (AttributeError, Exception) as e:
            response, code = create_response(
                status.HTTP_400_BAD_REQUEST, 'Not Found', e.args)
            return Response(response, status=code)


class UsersViewPublic(RetrieveAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializers

    def get(self, request, *args, **kwargs):
        users = self.get_queryset()
        serializers = UserSerializers(users, many=True)
        response, code = create_response(
            status.HTTP_200_OK, 'User Public', serializers.data)
        return Response(response, status=code)


class UserCreateView(CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = CreateUserSerializers

    def perform_create(self, serializer):
        password = make_password(self.request.data['password'])
        serializer.save(password=password)

    def post(self, request, *args, **kwargs):
        userSerializers = self.get_serializer(data=request.data)
        if userSerializers.is_valid():
            self.perform_create(userSerializers)
            response, code = create_response(
                status.HTTP_200_OK, 'User Create', userSerializers.data)
            return Response(userSerializers.data, status=code)
        response, code = create_response(
            status.HTTP_200_OK, 'Error', userSerializers.data)
        return Response(response, status=code)


class UserUpdateView(UpdateAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializers

    def get_object(self):
        try:
            request_user = self.kwargs['pk']
            user = Users.objects.get(pk=request_user)
            return user
        except Users.DoesNotExist:
            return None
        except Exception as e:
            response, code = create_response(
                status.HTTP_400_BAD_REQUEST, 'Error', e)
            return Response(response, status=code)

    def perform_update(self, serializer):
        serializer.save()

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        user = self.get_object()

        if user is None:
            response, code = create_response(
                status.HTTP_400_BAD_REQUEST, 'Password Error', 'User Not found')
            return Response(response, status=code)

        try:
            userSerializers = UserSerializers(
                user, data=request.data, partial=partial)
            if userSerializers.is_valid():
                self.perform_update(userSerializers)
                response, code = create_response(
                    status.HTTP_400_BAD_REQUEST, 'Password Error', 'User Not found')
                return Response(response, status=code)
            return Response(userSerializers.errors, 'Error', status=status.HTTP_400_BAD_REQUEST)
        except (AttributeError, Exception) as e:
            response, code = create_response(
                status.HTTP_400_BAD_REQUEST, 'Not Found', e.args)
            return Response(response, status=code)


class UserChangePasswordView(UpdateAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializers

    def get_object(self):
        try:
            request_user = self.kwargs['pk']
            user = Users.objects.get(pk=request_user)
            return user
        except (Users.DoesNotExist, TypeError):
            return None
        except (BaseException, TypeError) as e:
            return None

    def perform_update(self, serializer):
        if 'original-password' in self.request.data:
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()

    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        user = self.get_object()

        if user is None:
            response, code = create_response(
                status.HTTP_400_BAD_REQUEST, 'Not Found', e.args)
            return Response(response, status=code)

        if 'original-password' not in self.request.data:
            response, code = create_response(
                status.HTTP_400_BAD_REQUEST, 'Password Error', 'Password not found')
            return Response(response, status=code)

        if not user.check_password(request.data['original-password']):
            response, code = create_response(
                status.HTTP_400_BAD_REQUEST, 'Password Error', 'Password is not correct.')
            return Response(response, status=code)

        userSerializers = UserChangePassword(
            user, data=request.data, partial=partial, context={'context': request})

        try:
            if userSerializers.is_valid():
                self.perform_update(userSerializers)
                response, code = create_response(
                    status.HTTP_200_OK, 'Password', 'Password Change')
                return Response(response, status=code)
            return Response(userSerializers.errors, status=status.HTTP_400_BAD_REQUEST)
        except (AttributeError, Exception) as e:
            response, code = create_response(
                status.HTTP_400_BAD_REQUEST, 'Not Found', e.args)
            return Response(response, status=code)
