from rest_framework import serializers
from .models import Version, Directory

class RefbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Directory
        fields = ['id', 'code', 'name']


class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = ['version', 'start_date']


class DirectorySerializer(serializers.ModelSerializer):
    # versions = VersionSerializer(many=True, source='version_set',
    #                              read_only=True)
    class Meta:
        model = Directory
        fields = ['id', 'code', 'name']





