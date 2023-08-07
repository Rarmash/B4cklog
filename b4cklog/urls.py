from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='b4cklog-home'),
    path('about/', views.about, name='b4cklog-about'),
    path('register/', views.about, name='b4cklog-signup'),
    path('login/', views.about, name='b4cklog-login'),
    path('logout/', views.about, name='b4cklog-logout'),
    path('profile/', views.about, name='b4cklog-profile'),
]
