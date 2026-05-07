from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    # Read-only computed field: parsed skills list
    skills_list = serializers.SerializerMethodField()
    # Show recruiter's username, not user ID
    created_by_username = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'required_skills',
            'skills_list', 'is_active', 'created_by_username',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by_username']

    def get_skills_list(self, obj):
        #Return parsed skills as a list for easy frontend consumption.
        return obj.get_skills_list()

    def get_created_by_username(self, obj):
        #Return username string instead of user ID.
        return obj.created_by.username if obj.created_by else None

    def validate_required_skills(self, value):
       #Ensure at least one skill is provided.
        if not value or not value.strip():
            raise serializers.ValidationError("At least one required skill must be specified.")
        return value

    def create(self, validated_data):
        #Auto-assign the logged-in user as creator.
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['created_by'] = request.user
        return super().create(validated_data)


class JobListSerializer(serializers.ModelSerializer):
    #Lightweight serializer for list endpoints (better performance)
    skills_list = serializers.SerializerMethodField()
    application_count = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = ['id', 'title', 'required_skills', 'skills_list',
                  'application_count', 'is_active', 'created_at']

    def get_skills_list(self, obj):
        return obj.get_skills_list()

    def get_application_count(self, obj):
        #Show how many candidates have applied.
        return obj.applications.count()
