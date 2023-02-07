from ....models import Genders
from rest_framework.serializers import ModelSerializer, CharField


class GenderSerializers(ModelSerializer):
    name = CharField()

    class Meta:
        model = Genders
        exclude = ('createdAt', 'updateAt')
