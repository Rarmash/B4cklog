from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='b4cklog-home'),
    path('about/', views.about, name='b4cklog-about')
]
