from django.shortcuts import render
from auth_app.forms import UserForm, UserProfileInfoForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request, 'auth_app/index.html')


def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)  # To set the password in hash
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'auth_app/registration.html', {'user_form': user_form, 'profile_form': profile_form,
                                                          'registered': registered})


# View for login
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")  # "username" came from login html input element name.
        password = request.POST.get("password")  # "password" came from login html input element name.

        user = authenticate(username=username, password=password)

        # checking the user is passed the authentication
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return HttpResponse(" Account is not registered")

        else:
            print("someone tried to login and failed")
            print(f"Username:{username} and password: {password}")
            return HttpResponse("Invalid login details")

    else:
        return render(request, "auth_app/login.html")


# View for logout @login_required is given to ensure only login user can logout.
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))