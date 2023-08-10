from django.shortcuts import render, get_object_or_404
from .models import Game
from django.http import JsonResponse
from django.contrib.staticfiles.storage import staticfiles_storage
import random
from django.core.paginator import Paginator
from django.db.models import Q

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