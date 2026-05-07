from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Notification.objects.all().select_related('candidate', 'job')
        if self.request.query_params.get('unread') == 'true':
            qs = qs.filter(is_read=False)
        return qs

    def list(self, request, *args, **kwargs):
        #Add unread count to response
        response = super().list(request, *args, **kwargs)
        response.data['unread_count'] = Notification.objects.filter(is_read=False).count()
        return response


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def mark_read(request, pk):
    #Mark a single notification as read
    notification = get_object_or_404(Notification, pk=pk)
    notification.is_read = True
    notification.save()
    return Response({'id': pk, 'is_read': True})


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def mark_unread(request, pk):
    #Mark a single notification as unread
    notification = get_object_or_404(Notification, pk=pk)
    notification.is_read = False
    notification.save()
    return Response({'id': pk, 'is_read': False})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_all_read(request):
    #Mark all notifications as read in one operation
    count = Notification.objects.filter(is_read=False).update(is_read=True)
    return Response({'message': f'{count} notifications marked as read.'})
