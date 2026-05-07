from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Job
from .forms import JobForm


def job_list(request):
    jobs = Job.objects.filter(is_active=True)

    # Search filter
    query = request.GET.get('q', '').strip()
    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(required_skills__icontains=query) |
            Q(description__icontains=query)
        )

    # Pagination: 9 jobs per page (3×3 grid)
    paginator = Paginator(jobs, 9)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'jobs/job_list.html', {
        'page_obj': page_obj,
        'query': query,
        'total_count': jobs.count(),
    })


def job_detail(request, pk):
    #Single job detail page with applicant count
    job = get_object_or_404(Job, pk=pk, is_active=True)
    applicant_count = job.applications.count()
    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'applicant_count': applicant_count,
    })


@login_required
def job_create(request):
    #Create a new job posting (auth required)
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.created_by = request.user
            job.save()
            messages.success(request, f'Job "{job.title}" posted successfully!')
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobForm()
    return render(request, 'jobs/job_form.html', {'form': form, 'action': 'Create'})


@login_required
def job_edit(request, pk):
    #Edit an existing job posting
    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobForm(instance=job)
    return render(request, 'jobs/job_form.html', {'form': form, 'action': 'Edit', 'job': job})


@login_required
def job_delete(request, pk):
   #Soft-delete: mark job as inactive instead of removing from DB.
    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        job.is_active = False
        job.save()
        messages.success(request, f'Job "{job.title}" has been removed.')
        return redirect('job_list')
    return render(request, 'jobs/job_confirm_delete.html', {'job': job})
