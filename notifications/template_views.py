#Notifications HTML Views

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Notification


@login_required
def notification_list(request):
#Main notifications page
    notifications = Notification.objects.all().select_related('candidate', 'job')
    unread_count = notifications.filter(is_read=False).count()
    return render(request, 'notifications/notification_list.html', {
        'notifications': notifications,
        'unread_count': unread_count,
    })


@login_required
def toggle_read(request, pk):
    #Toggle read/unread state of a notification
    notification = get_object_or_404(Notification, pk=pk)
    notification.is_read = not notification.is_read
    notification.save()
    return redirect('notification_list')


@login_required
def mark_all_read(request):
    #Mark all as read
    Notification.objects.filter(is_read=False).update(is_read=True)
    messages.success(request, 'All notifications marked as read.')
    return redirect('notification_list')
