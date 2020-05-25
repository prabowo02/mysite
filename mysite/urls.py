from django.conf.urls import url, include

urlpatterns = [
    url(r'^tlxrating/', include('tlxrating.urls')),
]
