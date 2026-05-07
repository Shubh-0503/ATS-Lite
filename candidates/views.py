from rest_framework import viewsets, status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction

from .models import Candidate, Application
from .serializers import (
    CandidateSerializer, ApplicationSerializer,
    ApplicationWithScoreSerializer, ApplyToJobSerializer
)
from .utils import calculate_match_score
from jobs.models import Job
from notifications.models import Notification


class CandidateViewSet(viewsets.ReadOnlyModelViewSet):
    
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        #Optional: filter by min_score for a specific job.
        qs = Candidate.objects.all()
        return qs


@api_view(['POST'])
@permission_classes([AllowAny])  # Anyone can apply
def apply_to_job(request, job_id):
  
    job = get_object_or_404(Job, pk=job_id, is_active=True)

    serializer = ApplyToJobSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data

    with transaction.atomic():
        # Get or create candidate by email (idempotent)
        candidate, created = Candidate.objects.get_or_create(
            email=data['email'],
            defaults={
                'name': data['name'],
                'skills': data['skills'],
                'phone': data.get('phone', ''),
            }
        )

        # If candidate exists, update their skills (they may have added new ones)
        if not created:
            candidate.skills = data['skills']
            if data.get('phone'):
                candidate.phone = data['phone']
            candidate.save()

        # Check for duplicate application
        if Application.objects.filter(candidate=candidate, job=job).exists():
            return Response(
                {'error': f'You have already applied to "{job.title}".'},
                status=status.HTTP_409_CONFLICT
            )

        # Create the application
        application = Application.objects.create(
            candidate=candidate,
            job=job,
            cover_letter=data.get('cover_letter', ''),
            resume=data.get('resume'),
        )

        # Create notification for recruiter
        Notification.objects.create(
            message=f"New application: {candidate.name} applied for '{job.title}'.",
            candidate=candidate,
            job=job,
        )

    # Calculate and return score
    match_result = calculate_match_score(job.required_skills, candidate.skills)

    return Response({
        'message': f'Application submitted successfully!',
        'application_id': application.id,
        'candidate': {
            'id': candidate.id,
            'name': candidate.name,
            'email': candidate.email,
        },
        'job': {
            'id': job.id,
            'title': job.title,
        },
        'match_score': match_result['score'],
        'match_details': {
            'matched': match_result['matched'],
            'missing': match_result['missing'],
            'extra': match_result['extra'],
        }
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ranked_candidates(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    applications = Application.objects.filter(job=job).select_related('candidate')

    min_score = request.query_params.get('min_score')

    results = []
    for app in applications:
        details = app.get_match_details()
        score = details['score']

        if min_score is not None:
            try:
                if score < float(min_score):
                    continue
            except ValueError:
                pass

        results.append({
            'application_id': app.id,
            'candidate_id': app.candidate.id,
            'name': app.candidate.name,
            'email': app.candidate.email,
            'skills': app.candidate.get_skills_list(),
            'status': app.status,
            'match_score': score,
            'match_label': __import__('candidates.utils', fromlist=['get_score_label']).get_score_label(score),
            'matched_skills': details['matched'],
            'missing_skills': details['missing'],
            'applied_at': app.applied_at,
        })

    # Sort by score descending, then by application date (earliest first for ties)
    results.sort(key=lambda x: (-x['match_score'], x['applied_at']))

    return Response({
        'job_id': job.id,
        'job_title': job.title,
        'total': len(results),
        'candidates': results
    })


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_application_status(request, application_id):
    
    application = get_object_or_404(Application, pk=application_id)
    new_status = request.data.get('status')

    valid_statuses = [choice[0] for choice in Application.STATUS_CHOICES]
    if new_status not in valid_statuses:
        return Response(
            {'error': f'Invalid status. Choose from: {valid_statuses}'},
            status=status.HTTP_400_BAD_REQUEST
        )

    application.status = new_status
    application.save()
    return Response({'message': 'Status updated.', 'status': new_status})
