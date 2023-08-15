from django.shortcuts import render, get_object_or_404
from .models import Game
from django.http import JsonResponse
from django.contrib.staticfiles.storage import staticfiles_storage
import random
from django.core.paginator import Paginator
from django.db.models import Q
from users.models import Profile
from django.contrib.auth.decorators import login_required

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

def game_detail(request, igdb_id):
    game = get_object_or_404(Game, igdb_id=igdb_id)
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        backlog_section = request.POST.get('backlog_section')
        
        # Убираем игру из других категорий, если она там была
        for category in ['backlog_want_to_play', 'backlog_playing', 'backlog_played', 'backlog_completed', 'backlog_completed_100']:
            if category != backlog_section and game in getattr(user_profile, category).all():
                getattr(user_profile, category).remove(game)
        
        # Добавляем игру в выбранную категорию
        if backlog_section in ['backlog_want_to_play', 'backlog_playing', 'backlog_played', 'backlog_completed', 'backlog_completed_100']:
            getattr(user_profile, backlog_section).add(game)
    
    context = {
        'game': game
    }
    return render(request, 'b4cklog/game_detail.html', context)

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
    
    context = {
        'category': category,
        'games': games
    }
    return render(request, 'b4cklog/backlog_category.html', context)