from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Section


# Create your views here.
@login_required
def my_sections(request):
    if not hasattr(request.user, 'professor'):
        return HttpResponseForbidden("Not a professor account.")

    sections = request.user.professor.section_set.all()
    return render(request, 'courses/my_sections.html', {'sections': sections})