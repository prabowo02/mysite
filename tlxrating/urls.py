from django.conf.urls import url, include

from .views import tlxrating

urlpatterns = [
    url(r'^', tlxrating),
]
