#Django forms for Job model.

from django import forms
from .models import Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'required_skills', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'e.g. Senior Python Developer'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'rows': 4,
                'placeholder': 'Job description...'
            }),
            'required_skills': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'Python, Django, REST API, PostgreSQL'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-indigo-600'
            }),
        }
        help_texts = {
            'required_skills': 'Enter comma-separated skills.',
        }
