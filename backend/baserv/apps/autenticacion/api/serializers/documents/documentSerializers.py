from ....models import Document_types
from rest_framework.serializers import ModelSerializer

class DocumentSerializers(ModelSerializer):
    class Meta:
        model = Document_types
        fields = '__all__'
