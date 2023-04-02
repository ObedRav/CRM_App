from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def home(request) -> render.__class__:
    # Ckeck if logging in
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful')
        else:
            messages.error(request, 'Login failed')

        return redirect('home')

    else:
        return render(request, 'home.html', {})


def logout_user(request) -> redirect.__class__:
    logout(request)
    messages.success(request, 'You have been logged out')
    print(request.__class__.__name__)
    return redirect('home')