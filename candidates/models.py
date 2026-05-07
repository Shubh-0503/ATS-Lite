import os
from django.db import models
from django.core.validators import FileExtensionValidator
from jobs.models import Job
from candidates.utils import calculate_match_score


def resume_upload_path(instance, filename):
    return f'resumes/candidate_{instance.candidate.id}/{filename}'


class Candidate(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(
        unique=True,
        help_text="Used as unique identifier for the candidate"
    )
    skills = models.TextField(
        help_text="Comma-separated skills, e.g. 'Python, Django, REST API'"
    )
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} <{self.email}>"

    def get_skills_list(self):
        """Parse candidate skills into a clean list (same logic as Job)."""
        from candidates.utils import parse_skills
        return parse_skills(self.skills)


class Application(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('reviewed', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    ]

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    cover_letter = models.TextField(
        blank=True,
        help_text="Optional cover letter from candidate"
    )
    resume = models.FileField(
        upload_to=resume_upload_path,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],
        help_text="Resume file (PDF, DOC, DOCX)"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Prevent duplicate applications: one candidate per job
        unique_together = [('candidate', 'job')]
        ordering = ['-applied_at']
        indexes = [
            models.Index(fields=['job', 'status']),
            models.Index(fields=['candidate', '-applied_at']),
        ]

    def __str__(self):
        return f"{self.candidate.name} → {self.job.title}"

    def calculate_match_score(self) -> float:
       
        result = calculate_match_score(
            self.job.required_skills,
            self.candidate.skills
        )
        return result['score']

    def get_match_details(self) -> dict:
        return calculate_match_score(
            self.job.required_skills,
            self.candidate.skills
        )
