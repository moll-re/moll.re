from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('fetch_total_views', views.fetch_total_views, name='fetch_total_views'),
    path('fetch_relative_views', views.fetch_relative_views, name='fetch_relative_views'),
]