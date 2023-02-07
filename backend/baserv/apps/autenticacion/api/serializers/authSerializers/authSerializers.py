from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from ...serializers.Validators.userValidators import UserValidatorBefore
from ...serializers.roles.roleSerializers import RolesSimpleSerializers
from ....models import Persons, Users
from ...serializers.persons.personSerializers import PersonsSimpleSerializers
User = get_user_model()


class RegisterSerializers(serializers.ModelSerializer):

    username = serializers.SlugField(
        max_length=100,
        validators=[UniqueValidator(queryset=Users.objects.all())]
    )
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        model = Users
        fields = '__all__'
        validators = [UserValidatorBefore()]

    person = PersonsSimpleSerializers()

    def create(self, validated_data):
        person = validated_data.pop('person')
        user = Users.objects.create(**validated_data)
        Persons.objects.create(**person, user=user)
        return user


class LoginSerializers(serializers.ModelSerializer):
    email = serializers.CharField(label='Email/username')
    password = serializers.CharField()
    roles = RolesSimpleSerializers(many=True, required=False)

    class Meta:
        model = Users
        fields = ('id', 'password', 'email', 'roles')

    def validate(self, attrs):
        user = authenticate(**attrs)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Incorrect Credentials Passed.')
