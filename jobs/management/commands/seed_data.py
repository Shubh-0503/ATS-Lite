from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from jobs.models import Job
from candidates.models import Candidate, Application
from notifications.models import Notification


SAMPLE_JOBS = [
    {
        "title": "Senior Python Developer",
        "description": "Build scalable backend APIs for our fintech platform.",
        "required_skills": "Python, Django, REST API, PostgreSQL, Docker",
    },
    {
        "title": "Frontend React Developer",
        "description": "Build beautiful, responsive UIs for our SaaS product.",
        "required_skills": "React, JavaScript, TypeScript, Tailwind CSS, HTML",
    },
    {
        "title": "DevOps Engineer",
        "description": "Manage cloud infrastructure and CI/CD pipelines.",
        "required_skills": "Docker, Kubernetes, AWS, Linux, Terraform, CI/CD",
    },
    {
        "title": "Data Scientist",
        "description": "Build ML models and analyze large datasets.",
        "required_skills": "Python, Pandas, Scikit-learn, SQL, Machine Learning, TensorFlow",
    },
    {
        "title": "Full Stack Developer",
        "description": "Work on both frontend and backend features.",
        "required_skills": "Python, Django, React, PostgreSQL, REST API",
    },
]

SAMPLE_CANDIDATES = [
    {"name": "Alice Sharma",  "email": "alice@example.com",  "skills": "Python, Django, REST API, PostgreSQL, Docker"},
    {"name": "Bob Verma",     "email": "bob@example.com",    "skills": "Python, Django, REST API"},
    {"name": "Carol Singh",   "email": "carol@example.com",  "skills": "React, JavaScript, TypeScript, HTML, Tailwind CSS"},
    {"name": "David Nair",    "email": "david@example.com",  "skills": "Python, Pandas, SQL, Machine Learning"},
    {"name": "Eva Patel",     "email": "eva@example.com",    "skills": "Docker, Kubernetes, AWS, Linux"},
    {"name": "Frank Kumar",   "email": "frank@example.com",  "skills": "Python, Django, React, PostgreSQL"},
    {"name": "Grace Thomas",  "email": "grace@example.com",  "skills": "JavaScript, React, HTML"},
    {"name": "Henry Mehta",   "email": "henry@example.com",  "skills": "Python, SQL, Pandas, TensorFlow, Scikit-learn, Machine Learning"},
]


class Command(BaseCommand):
    help = 'Seed database with sample jobs, candidates, and applications'

    def handle(self, *args, **options):
        self.stdout.write('🌱 Seeding database...')

        # Get or create admin user
        admin, _ = User.objects.get_or_create(
            username='admin',
            defaults={'is_staff': True, 'is_superuser': True, 'email': 'admin@example.com'}
        )
        if _:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write('  ✓ Created admin user (password: admin123)')

        # Create jobs
        jobs = []
        for job_data in SAMPLE_JOBS:
            job, created = Job.objects.get_or_create(
                title=job_data['title'],
                defaults={**job_data, 'created_by': admin}
            )
            jobs.append(job)
            if created:
                self.stdout.write(f'  ✓ Job: {job.title}')

        # Create candidates
        candidates = []
        for cand_data in SAMPLE_CANDIDATES:
            cand, created = Candidate.objects.get_or_create(
                email=cand_data['email'],
                defaults=cand_data
            )
            candidates.append(cand)
            if created:
                self.stdout.write(f'  ✓ Candidate: {cand.name}')

        # Create some applications (realistic combinations)
        applications = [
            (0, 0), (0, 1), (0, 5),  # Python job applicants
            (1, 2), (1, 6),           # React job applicants
            (2, 4),                   # DevOps applicant
            (3, 3), (3, 7),           # Data Science applicants
            (4, 5), (4, 0),           # Full Stack applicants
        ]

        app_count = 0
        for job_idx, cand_idx in applications:
            job = jobs[job_idx]
            candidate = candidates[cand_idx]
            app, created = Application.objects.get_or_create(
                candidate=candidate,
                job=job
            )
            if created:
                # Create notification
                Notification.objects.get_or_create(
                    candidate=candidate,
                    job=job,
                    defaults={
                        'message': f"New application: {candidate.name} applied for '{job.title}'."
                    }
                )
                app_count += 1

        self.stdout.write(f'  ✓ Created {app_count} applications with notifications')
        self.stdout.write(self.style.SUCCESS('\n Database seeded successfully!'))
        self.stdout.write('   Login at http://127.0.0.1:8000/admin/ with admin / admin123')
