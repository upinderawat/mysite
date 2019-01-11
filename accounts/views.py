from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import UserProfileForm, UserForm
from django.http import HttpResponseRedirect, HttpResponse
# Create your views here.
def register(request):
    registered = False
    if request.method == 'POST':
        profile_form = UserProfileForm(data=request.POST)
        user_form = UserForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'accounts/register.html', context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered })

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Your account temporarily Disabled')
        else:
            return HttpResponse("Username password mismatch")
    else:
        return render(request, 'accounts/login.html',{})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
