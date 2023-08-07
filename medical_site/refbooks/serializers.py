from rest_framework import serializers
from .models import Directory, Element


class DirectorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Directory
        fields = ["id", "code", "name"]


class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = ["element_code", "element_value"]


class CheckElementSerializer(serializers.Serializer):
    code = serializers.CharField()
    value = serializers.CharField()
    version = serializers.CharField(required=False)
