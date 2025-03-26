from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
import hashlib
import os
from datetime import datetime

class Evidence(models.Model):
    EVIDENCE_TYPES = [
        ('VIDEO', 'Video'),
        ('IMAGE', 'Image'),
        ('DOCUMENT', 'Document'),
        ('AUDIO', 'Audio'),
        ('OTHER', 'Other'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(
        upload_to='evidence/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'jpg', 'jpeg', 'png', 'pdf', 'doc', 'docx', 'mp3', 'wav'])]
    )
    evidence_type = models.CharField(max_length=10, choices=EVIDENCE_TYPES)
    uploaded_by = models.ForeignKey(User, on_delete=models.PROTECT)
    upload_date = models.DateTimeField(auto_now_add=True)
    file_hash = models.CharField(max_length=64)  # SHA-256 hash
    case_number = models.CharField(max_length=50)
    is_immutable = models.BooleanField(default=True)
    file_size = models.BigIntegerField()
    mime_type = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only on creation
            # Calculate file hash
            sha256_hash = hashlib.sha256()
            with self.file.open("rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            self.file_hash = sha256_hash.hexdigest()
            
            # Get file size and mime type
            self.file_size = self.file.size
            self.mime_type = self.file.content_type

        super().save(*args, **kwargs)

    def verify_integrity(self):
        """Verify the file hasn't been tampered with"""
        current_hash = hashlib.sha256()
        with self.file.open("rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                current_hash.update(byte_block)
        return current_hash.hexdigest() == self.file_hash

    def __str__(self):
        return f"{self.title} - {self.case_number}"

class EvidenceAccess(models.Model):
    evidence = models.ForeignKey(Evidence, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    granted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='access_grants')
    granted_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    access_level = models.CharField(max_length=20, choices=[
        ('VIEW', 'View Only'),
        ('DOWNLOAD', 'Download'),
        ('SHARE', 'Share'),
    ])
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.evidence.title}"

class AuditLog(models.Model):
    ACTION_TYPES = [
        ('UPLOAD', 'Upload'),
        ('VIEW', 'View'),
        ('DOWNLOAD', 'Download'),
        ('SHARE', 'Share'),
        ('DELETE', 'Delete'),
        ('MODIFY', 'Modify'),
    ]

    evidence = models.ForeignKey(Evidence, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=ACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    details = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.evidence.title}"

    class Meta:
        ordering = ['-timestamp']
