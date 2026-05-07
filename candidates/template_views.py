from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from .models import Candidate, Application
from .utils import calculate_match_score, get_score_label
from jobs.models import Job


def apply_form(request, job_id):
    #Display and handle the job application form.
    job = get_object_or_404(Job, pk=job_id, is_active=True)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        skills = request.POST.get('skills', '').strip()
        phone = request.POST.get('phone', '').strip()
        cover_letter = request.POST.get('cover_letter', '').strip()
        resume = request.FILES.get('resume')

        # Validation
        errors = []
        if not name:
            errors.append('Name is required.')
        if not email:
            errors.append('Email is required.')
        if not skills:
            errors.append('Please list at least one skill.')

        if resume:
            # Basic file size check (5MB)
            if resume.size > 5 * 1024 * 1024:
                errors.append('Resume file must be under 5MB.')
            allowed_ext = ['.pdf', '.doc', '.docx']
            import os
            ext = os.path.splitext(resume.name)[1].lower()
            if ext not in allowed_ext:
                errors.append('Resume must be PDF, DOC, or DOCX.')

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'candidates/apply_form.html', {
                'job': job, 'post_data': request.POST
            })

        # Get or create candidate
        candidate, _ = Candidate.objects.get_or_create(
            email=email,
            defaults={'name': name, 'skills': skills, 'phone': phone}
        )
        candidate.skills = skills
        candidate.save()

        # Check duplicate
        if Application.objects.filter(candidate=candidate, job=job).exists():
            messages.warning(request, f'You have already applied to "{job.title}".')
            return redirect('job_detail', pk=job.pk)

        # Create application
        app = Application(
            candidate=candidate, job=job,
            cover_letter=cover_letter
        )
        if resume:
            app.resume = resume
        app.save()

        # Notification
        from notifications.models import Notification
        Notification.objects.create(
            message=f"New application: {candidate.name} applied for '{job.title}'.",
            candidate=candidate,
            job=job,
        )

        # Calculate score to show on confirmation
        score = app.calculate_match_score()
        messages.success(request, f'Application submitted! Your skill match: {score}%')
        return redirect('application_success', app_id=app.pk)

    return render(request, 'candidates/apply_form.html', {'job': job})


def application_success(request, app_id):
    """Confirmation page after successful application."""
    app = get_object_or_404(Application, pk=app_id)
    details = app.get_match_details()
    label = get_score_label(details['score'])
    return render(request, 'candidates/application_success.html', {
        'application': app,
        'details': details,
        'label': label,
    })


@login_required
def candidate_list(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    applications = Application.objects.filter(job=job).select_related('candidate')

    # Build ranked list
    min_score = request.GET.get('min_score', '')
    ranked = []
    for app in applications:
        details = app.get_match_details()
        score = details['score']
        if min_score:
            try:
                if score < float(min_score):
                    continue
            except ValueError:
                pass
        ranked.append({
            'application': app,
            'score': score,
            'label': get_score_label(score),
            'matched': details['matched'],
            'missing': details['missing'],
        })

    ranked.sort(key=lambda x: -x['score'])

    # Pagination
    paginator = Paginator(ranked, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'candidates/candidate_list.html', {
        'job': job,
        'page_obj': page_obj,
        'min_score': min_score,
        'total': len(ranked),
    })
