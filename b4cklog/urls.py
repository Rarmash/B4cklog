from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'platforms', views.PlatformViewSet)
router.register(r'games', views.GameViewSet)

urlpatterns = [
    path('', views.home, name='b4cklog-home'),
    path('about/', views.about, name='b4cklog-about'),
    path('register/', views.about, name='b4cklog-signup'),
    path('login/', views.about, name='b4cklog-login'),
    path('logout/', views.about, name='b4cklog-logout'),
    path('profile/', views.about, name='b4cklog-profile'),
    path('game/<int:igdb_id>/', views.game_detail, name='game_detail'),
    path('search/', views.game_search, name='game_search'),
    path('search/results/', views.search_results, name='search_results'),
    path('backlog/<str:category>/', views.backlog_category, name='backlog_category'),
    # path('save-rating/', views.save_rating, name='save_rating'),
    path('api/', include(router.urls)),
    path('api/games/', views.GameListView.as_view(), name='api-game-list'),
    path('api/game/<int:igdb_id>/', views.GameDetailView.as_view(), name='api-game-detail'),
]
