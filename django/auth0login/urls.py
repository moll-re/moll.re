from django.urls import path,include
from . import views


urlpatterns = [
    path('profile', views.profile),
    path('logout', views.logout),
    path('', include('django.contrib.auth.urls')),
    path('', include('social_django.urls')),
]
