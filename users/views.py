from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your accout created. You can log in using your username: {username}')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def redirect_to_own_profile(request):
    return redirect('profile', username=request.user.username)

@login_required
def profile(request, username):
    user = get_object_or_404(User, username__iexact=username)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your profile has been successfully updated.')
            return redirect('profile', username=username)
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=user.profile)

    context = {
        'user': user,
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'users/profile.html', context)