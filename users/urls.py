from django.urls import path
from .views import ProfileDetailView

urlpatterns = [
    path('api/profile/', ProfileDetailView.as_view(), name='profile-detail'),
]
