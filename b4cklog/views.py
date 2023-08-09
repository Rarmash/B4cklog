from django.shortcuts import render, get_object_or_404
from .models import Game

def home(request):
    context = {
		'games': Game.objects.all()
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
