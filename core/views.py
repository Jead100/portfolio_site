from django.shortcuts import render
from .models import Bio, Project

def home(request):
    bio = Bio.objects.first()
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'core/home.html', {'bio': bio, 'projects': projects})
