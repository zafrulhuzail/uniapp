from django.urls import path
from .views import my_sections

urlpatterns = [
    path("my-sections/", my_sections),
]
