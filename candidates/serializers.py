

from rest_framework import serializers
from .models import Candidate, Application
from .utils import calculate_match_score, get_score_label
from jobs.serializers import JobListSerializer


class CandidateSerializer(serializers.ModelSerializer):
    skills_list = serializers.SerializerMethodField()
    application_count = serializers.SerializerMethodField()

    class Meta:
        model = Candidate
        fields = ['id', 'name', 'email', 'phone', 'skills', 'skills_list',
                  'application_count', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_skills_list(self, obj):
        return obj.get_skills_list()

    def get_application_count(self, obj):
        return obj.applications.count()

    def validate_email(self, value):
        #Normalize email to lowercase.
        return value.lower().strip()


class ApplicationSerializer(serializers.ModelSerializer):
    #Used for creating and updating applications.
    # Allow writing by ID, read as nested object
    candidate_detail = CandidateSerializer(source='candidate', read_only=True)
    job_title = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = ['id', 'candidate', 'candidate_detail', 'job', 'job_title',
                  'cover_letter', 'resume', 'status', 'applied_at']
        read_only_fields = ['id', 'applied_at']

    def get_job_title(self, obj):
        return obj.job.title

    def validate(self, attrs):
        #Prevent duplicate applications.
        candidate = attrs.get('candidate')
        job = attrs.get('job')

        # On create (no instance), check for existing application
        if not self.instance:
            if Application.objects.filter(candidate=candidate, job=job).exists():
                raise serializers.ValidationError(
                    f"{candidate.name} has already applied to '{job.title}'."
                )
        return attrs


class ApplicationWithScoreSerializer(serializers.ModelSerializer):
   
    candidate_name = serializers.CharField(source='candidate.name', read_only=True)
    candidate_email = serializers.CharField(source='candidate.email', read_only=True)
    candidate_skills = serializers.CharField(source='candidate.skills', read_only=True)
    match_score = serializers.SerializerMethodField()
    match_label = serializers.SerializerMethodField()
    match_details = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = [
            'id', 'candidate', 'candidate_name', 'candidate_email',
            'candidate_skills', 'job', 'status', 'match_score',
            'match_label', 'match_details', 'applied_at'
        ]

    def get_match_score(self, obj):
        return obj.calculate_match_score()

    def get_match_label(self, obj):
        score = obj.calculate_match_score()
        return get_score_label(score)

    def get_match_details(self, obj):
        #Full breakdown: matched, missing, extra skills.
        details = obj.get_match_details()
        # Remove redundant raw strings from response
        return {
            'matched': details['matched'],
            'missing': details['missing'],
            'extra': details['extra'],
        }


class ApplyToJobSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    skills = serializers.CharField(help_text="Comma-separated skills")
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    cover_letter = serializers.CharField(required=False, allow_blank=True)
    resume = serializers.FileField(required=False, allow_null=True)

    def validate_email(self, value):
        return value.lower().strip()
