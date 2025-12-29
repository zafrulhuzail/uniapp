from django.urls import path
from .views import list_course_timetable, student_timetable, my_timetable, day_view
from .api_views import *
from .views_dragdrop import show_enrollment, hide_enrollment
from .views_personal_events import (
    personal_event_create,
    personal_event_update,
    personal_event_delete,
)

urlpatterns = [
    path("student/<int:student_id>/timetable/", student_timetable, name="student_timetable"),
    path("me/", my_timetable, name="my_timetable"),   
    path("me/list", list_course_timetable, name="list_course_timetable"),   
    path("me/day_view/", day_view, name="day_view"),   
    path("api/me/", api_my_timetable, name="api_my_timetable"),
    path("api/me/day_view/", api_day_view, name="api_day_view"),
    path("api/me/mandatory_course/", api_my_timetable_mandatory_course, name="api_my_timetable_mandatory_course"),
    path("api/me/elective_course/", api_my_timetable_elective_course, name="api_my_timetable_elective_course"),
    path("api/me/activate_show_on_timetable/<int:enrollment_id>/", api_activate_show_on_timetable, name="api_activate_show_on_timetable"),
    path("enrollment/<int:enrollment_id>/show/", show_enrollment, name="show_enrollment"),
    path("enrollment/<int:enrollment_id>/hide/", hide_enrollment, name="hide_enrollment"),
    path("personal/create/", personal_event_create, name="personal_event_create"),
    path("personal/<int:event_id>/update/", personal_event_update, name="personal_event_update"),
    path("personal/<int:event_id>/delete/", personal_event_delete, name="personal_event_delete"),
]