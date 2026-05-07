from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Q

from .models import Job
from .serializers import JobSerializer, JobListSerializer


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'required_skills', 'description']
    ordering_fields = ['created_at', 'title']

    def get_serializer_class(self):
        #Use lightweight serializer for list, full for detail/create/update
        if self.action == 'list':
            return JobListSerializer
        return JobSerializer

    def get_queryset(self):
        qs = Job.objects.all()
        active_param = self.request.query_params.get('active')
        if active_param is not None:
            qs = qs.filter(is_active=active_param.lower() == 'true')
        return qs

    @action(detail=False, methods=['get'], url_path='active')
    def active_jobs(self, request):
       #Return only active job listings
        jobs = Job.objects.filter(is_active=True)
        page = self.paginate_queryset(jobs)
        serializer = JobListSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['get'], url_path='applicants')
    def applicants(self, request, pk=None):
        job = self.get_object()
        from candidates.models import Application
        from candidates.serializers import ApplicationWithScoreSerializer

        applications = Application.objects.filter(job=job).select_related('candidate')

        # Optional minimum score filter
        min_score = request.query_params.get('min_score')

        # Calculate scores and sort
        app_data = []
        for app in applications:
            score = app.calculate_match_score()
            if min_score is None or score >= float(min_score):
                app_data.append((app, score))

        # Sort by score descending
        app_data.sort(key=lambda x: x[1], reverse=True)

        # Paginate
        result = []
        for app, score in app_data:
            serializer = ApplicationWithScoreSerializer(app)
            data = serializer.data
            data['match_score'] = score
            result.append(data)

        return Response({
            'job': job.title,
            'total_applicants': len(result),
            'applicants': result
        })
