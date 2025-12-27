from django.urls import path
from .views import student_timetable, my_timetable, day_view
from .api_views import api_my_timetable, api_day_view

urlpatterns = [
    path("student/<int:student_id>/timetable/", student_timetable, name="student_timetable"),
    path("me/", my_timetable, name="my_timetable"),   
    path("me/day_view/", day_view, name="day_view"),   
    path("api/me/", api_my_timetable, name="api_my_timetable"),
    path("api/me/day_view/", api_day_view, name="api_day_view"),
]