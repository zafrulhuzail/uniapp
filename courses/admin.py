from django.contrib import admin
from .models import Course, Section, SectionMeeting, Enrollment
# Register your models here.

admin.site.register(Course)
admin.site.register(Section)
admin.site.register(SectionMeeting)
admin.site.register(Enrollment)