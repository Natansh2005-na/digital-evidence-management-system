from rest_framework import serializers
from .models import Evidence, EvidenceAccess
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class EvidenceSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)
    file_size = serializers.SerializerMethodField()
    file_hash = serializers.CharField(read_only=True)
    is_immutable = serializers.BooleanField(read_only=True)

    class Meta:
        model = Evidence
        fields = [
            'id', 'title', 'description', 'file', 'evidence_type',
            'uploaded_by', 'upload_date', 'file_hash', 'case_number',
            'is_immutable', 'file_size', 'mime_type'
        ]
        read_only_fields = ['upload_date', 'file_hash', 'is_immutable', 'file_size', 'mime_type']

    def get_file_size(self, obj):
        return obj.file_size

class EvidenceAccessSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    granted_by = UserSerializer(read_only=True)
    evidence = EvidenceSerializer(read_only=True)

    class Meta:
        model = EvidenceAccess
        fields = [
            'id', 'evidence', 'user', 'granted_by', 'granted_date',
            'expiry_date', 'access_level', 'is_active'
        ]
        read_only_fields = ['granted_date'] 