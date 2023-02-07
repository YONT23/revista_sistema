from ....models import *
from rest_framework.serializers import ModelSerializer, Serializer, IntegerField
from .....helpers.menuResources import menuResources


class ResourcesSerializers(ModelSerializer):
    class Meta:
        model = Resources
        exclude = ('roles',)


class ResourcesRolesSerializers(Serializer):
    rolesId = IntegerField()
    resources = ResourcesSerializers(many=True)

    def create(self, validated_data):
        try:
            resources = []
            list_resources_roles = []

            id_last_resources = 0
            last = Resources.objects.last()
            if last:
                id_last_resources = last.id
            
            menuResources(validated_data['resources'],
                          resources, Resources, id_last_resources)

            resources = Resources.objects.bulk_create(resources)

            roles = Roles.objects.get(pk=validated_data['rolesId'])
            
            for r in resources:
                list_resources_roles.append(Resources_roles(
                    rolesId=roles, resourcesId=r))

            Resources_roles.objects.bulk_create(list_resources_roles)
            return None
        except Exception as e:
            raise e
