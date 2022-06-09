from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

    return render(request, 'users/login.html')


def register_page(request):
    form = RegisterUserForm()
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()

    return render(request, 'users/register.html', {
        'form': form
    })
