from base.models import Footages
from  rest_framework import serializers

class FootagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Footages
        fields = ['footage', 'user']  