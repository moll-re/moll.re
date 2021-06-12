from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:post_id>/', views.expand_post, name='detail'),
]