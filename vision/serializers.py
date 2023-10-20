from rest_framework import serializers
from .models import Modelo

class ModeloSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Modelo
        fields = '__all__'
    