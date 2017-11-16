from rest_framework import serializers

from arquivo.models import Arquivo


class ArquivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arquivo
        fields = ['uuid', 'created_at', 'updated_at', 'arquivo']
