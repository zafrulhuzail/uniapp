from django import urls
from .views import signup

urlpatterns = [
    urls.path('signup/', signup),
]