#Notifications serializers

from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(source='candidate.name', read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True, allow_null=True)

    class Meta:
        model = Notification
        fields = ['id', 'message', 'is_read', 'candidate', 'candidate_name',
                  'job', 'job_title', 'created_at']
        read_only_fields = ['id', 'created_at', 'candidate_name', 'job_title']
