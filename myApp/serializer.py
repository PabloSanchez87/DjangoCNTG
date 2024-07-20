from rest_framework import serializers
from myApp.models import irisModel

class irisSerializer(serializers.ModelSerializer):
    class Meta:
        model = irisModel
        fields = '__all__'
