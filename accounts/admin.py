from django.contrib import admin
from .models import Student, Professor, Semester

# Register your models here.
admin.site.register(Student)
admin.site.register(Professor)
admin.site.register(Semester)
