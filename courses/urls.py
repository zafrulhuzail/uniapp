from django.urls import path
from .views import *
from .api_views import *

urlpatterns = [
    path("my-sections/", my_sections),
    path("api/mandatory-courses/", get_mandatory_courses, name="mandatory_courses"),
    path("api/elective-courses/", get_elective_courses, name="elective_courses"),
    path("api/get-enrollments/", api_get_enrolled_courses, name="api_get_enrolled_courses"),
]
