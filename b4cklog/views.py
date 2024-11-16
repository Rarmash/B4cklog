from django.shortcuts import render, get_object_or_404
from .models import Platform, Game
from django.http import JsonResponse
from django.contrib.staticfiles.storage import staticfiles_storage
import random
from django.core.paginator import Paginator
from django.db.models import Q
from users.models import Profile
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import PlatformSerializer, GameSerializer, GameRatingSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

def home(request):
    all_games = Game.objects.all()
    randomized_games = random.sample(list(all_games), len(all_games))  # Рандомизация списка игр
    paginator = Paginator(randomized_games, 60)  # 6 игр в ряду

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'games': page
    }
    return render(request, 'b4cklog/home.html', context)


def about(request):
    return render(request, 'b4cklog/about.html', {'title': 'About B4cklog'})


@login_required
def game_detail(request, igdb_id):
    game = get_object_or_404(Game, igdb_id=igdb_id)
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        # Updating backlog section
        backlog_section = request.POST.get('backlog_section')

        # Убираем игру из других категорий, если она там была
        for category in ['backlog_want_to_play', 'backlog_playing', 'backlog_played', 'backlog_completed',
                         'backlog_completed_100']:
            if category != backlog_section and game in getattr(user_profile, category).all():
                getattr(user_profile, category).remove(game)

        # Добавляем игру в выбранную категорию
        if backlog_section in ['backlog_want_to_play', 'backlog_playing', 'backlog_played', 'backlog_completed',
                               'backlog_completed_100', 'mark1']:
            getattr(user_profile, backlog_section).add(game)

    context = {
        'game': game
    }
    return render(request, 'b4cklog/game_detail.html', context)


# @login_required
# @require_POST
# def save_rating(request):
#     game_id = request.POST.get('game_id')
#     rating = request.POST.get('rating')
#
#     if not game_id or not rating:
#         return HttpResponseBadRequest("Missing game_id or rating")
#
#     game = get_object_or_404(Game, pk=game_id)
#     user = request.user
#
#     # Проверяем, есть ли у пользователя уже оценка для этой игры, и обновляем, если есть
#     try:
#         game_rating = GameRating.objects.get(user=user, game=game)
#     except GameRating.DoesNotExist:
#         game_rating = GameRating(user=user, game=game)
#
#     game_rating.rating = rating
#     game_rating.save()
#
#     return redirect('game_detail', igdb_id=game.igdb_id)

@login_required
@require_POST
def remove_game(request):
    game_id = request.POST.get('game_id')
    game = get_object_or_404(Game, pk=game_id)
    user_profile = Profile.objects.get(user=request.user)
    for category in ['backlog_want_to_play', 'backlog_playing', 'backlog_played', 'backlog_completed',
                     'backlog_completed_100']:
        getattr(user_profile, category).remove(game)

def game_search(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        q = request.GET.get('term', '')
        games = Game.objects.filter(name__icontains=q)
        results = []
        for game in games:
            game_json = {
                'id': game.igdb_id,
                'label': game.name,
                'cover': game.cover if game.cover else staticfiles_storage.url('default_cover.jpg'),
                'release_date': f"({str(game.first_release_date.strftime('%Y'))})" if game.first_release_date else ''
            }
            results.append(game_json)
        return JsonResponse(results, safe=False)
    return render(request, 'b4cklog/base.html')  # Исправлен путь к шаблону


def search_results(request):
    term = request.GET.get('term')
    games = Game.objects.filter(Q(name__icontains=term) | Q(summary__icontains=term))

    context = {
        'term': term,
        'games': games,
    }

    return render(request, 'b4cklog/search_results.html', context)


@login_required
def backlog_category(request, category):
    user = request.user
    profile = Profile.objects.get(user=user)
    games = profile.get_backlog_by_category(category)
    match category:
        case "backlog_want_to_play":
            category_name = "Want to play"
        case "backlog_playing":
            category_name = "Playing"
        case "backlog_played":
            category_name = "Played"
        case "backlog_completed":
            category_name = "Completed"
        case "backlog_completed_100":
            category_name = "Completed (100% achievements)"

    context = {
        'category': category,
        'category_name': category_name,
        'games': games
    }
    return render(request, 'b4cklog/backlog_category.html', context)

###############

class PlatformViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class GameListView(APIView):
    def get(self, request):
        games = list(Game.objects.all())
        random.shuffle(games)  # Перемешиваем игры
        paginator = PageNumberPagination()
        paginator.page_size = 60  # По 60 игр на страницу
        result_page = paginator.paginate_queryset(games, request)
        serializer = GameSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)