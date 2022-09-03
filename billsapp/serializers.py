from rest_framework import serializers

from .models import Bill, Client


class UploadSerializer(serializers.Serializer):
    file_uploaded = serializers.FileField()

    class Meta:
        fields = ['file_uploaded']


class BillSerializer(serializers.ModelSerializer):
    client = serializers.CharField(source="client.name")
    organization = serializers.CharField(source="organization.name")
    service = serializers.CharField(source="service.name")

    class Meta:
        model = Bill
        fields = [
            'id',
            'client',
            'organization',
            'num',
            'sum',
            'date',
            'service',
        ]
