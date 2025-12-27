from django.urls import path
from .views import student_timetable, my_timetable

urlpatterns = [
    path("student/<int:student_id>/timetable/", student_timetable, name="student_timetable"),
    path("me/", my_timetable, name="my_timetable"),   
]