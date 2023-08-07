from django.shortcuts import render
from .models import Game

games = [
    {
		'name': 'Halo 7',
		'release_date': 'Dec 31, 2999'
	},
	{
		'name': 'Small RPG',
		'release_date': 'Never'
	}
]

def home(request):
    context = {
		'games': Game.objects.all()
	}
    return render(request, 'b4cklog/home.html', context)
 
def about(request):
	return render(request, 'b4cklog/about.html', {'title': 'About B4cklog'})