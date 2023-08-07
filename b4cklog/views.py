from django.shortcuts import render


def home(request):
	return render(request, 'b4cklog/home.html', {'title': 'Home'})
 
def about(request):
	return render(request, 'b4cklog/about.html', {'title': 'About B4cklog'})