from django.urls import path
from .views import student_timetable

urlpatterns = [
    path("student/<int:student_id>/timetable/", student_timetable, name="student_timetable"),   
]