from rest_framework.views import APIView
from apps.autenticacion.api.serializers.authSerializers.authSerializers import LoginSerializers, RegisterSerializers
from apps.autenticacion.api.serializers.resources.resourceSerializer import ResourcesSerializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout
from .....helpers.createResponse import create_response
from rest_framework import status
from .....helpers.flat_List import flatList
from django.contrib.auth import login
from django.http import HttpResponse

class AuthLogin(APIView):
    serializer_class = LoginSerializers

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def post(self, request, *args, **kwargs):
        data = {}
        if 'email' in request.data:
            data['username'] = request.data['email']
            data['password'] = request.data['password']
        else:
            data = request.data

        serializers = LoginSerializers(
            data=data, context={'request': self.request})
        if not serializers.is_valid():
            response, code = create_response(
                status.HTTP_400_BAD_REQUEST, 'Error', serializers.errors)
            return Response(response, status=code)
        login(request, serializers.validated_data)
        token = self.get_tokens_for_user(serializers.validated_data)

        roles_ids = serializers.validated_data.roles.all()
        resources = [e.resources.prefetch_related(
            'resources') for e in roles_ids ]
        resources = flatList(resources)
        resources_unique = []
        [resources_unique.append(x) for x in resources if x not in resources_unique]
        menu = ResourcesSerializers(resources_unique, many=True)
        request.session['refresh-token'] = token['refresh']
        response, code = create_response(
            status.HTTP_200_OK, 'Login Success', {'token': token, 'user': {'name': serializers.validated_data.username,
                                                                           'id': serializers.validated_data.id},
                                                  'menu': menu.data})
        return Response(response, status=code)


class AuthRegister(APIView):
    serializer_class = RegisterSerializers

    def post(self, request, *args, **kwargs):
        registerUser = RegisterSerializers(data=request.data)
        if registerUser.is_valid():
            password = make_password(
                registerUser.validated_data['password'])
            registerUser.save(password=password)
            response, code = create_response(
                status.HTTP_200_OK, 'User Register', 'Registro Exitosos')
            return Response(response, status=code)
        response, code = create_response(
            status.HTTP_400_BAD_REQUEST, 'Error', registerUser.errors)
        return Response(response, status=code)


class LogoutView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            jwt_token = request.session.get('refresh-token', None)
            resp = HttpResponse('content')
            resp.cookies.clear()
            resp.flush()
            token = RefreshToken(jwt_token)
            token.blacklist()
            logout(request)
            request.session.clear()
            resp.flush()
            request.session.flush()
            response, code = create_response(
                status.HTTP_200_OK, 'Logout Success', 'Ok')
            return Response(response, code)
        except TokenError as TkError:
            response, code = create_response(
                status.HTTP_400_BAD_REQUEST, 'Error', f'{TkError}')
            return Response(response, code)
        except Exception as e:
            response, code = create_response(
                status.HTTP_400_BAD_REQUEST, 'Error', e)
            return Response(e.args, code)
