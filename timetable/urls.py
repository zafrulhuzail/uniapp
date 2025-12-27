from django.urls import path
from .views import student_timetable, my_timetable, day_view

urlpatterns = [
    path("student/<int:student_id>/timetable/", student_timetable, name="student_timetable"),
    path("me/", my_timetable, name="my_timetable"),   
    path("me/day_view/", day_view, name="day_view"),   
]