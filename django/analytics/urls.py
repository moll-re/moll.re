from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('fetch_total_views', views.fetch_total_views, name='fetch_total_views'),
    path('fetch_relative_views', views.fetch_relative_views, name='fetch_relative_views'),
    path('fetch_aio_sensors', views.fetch_aio_sensors, name='fetch_aio_sensors'),
    path('fetch_aio_bot_stats', views.fetch_aio_bot_stats, name='fetch_aio_bot_stats'),
    path('fetch_aio_lists/<id>', views.fetch_aio_lists, name='fetch_aio_lists'),
]