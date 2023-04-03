from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignupForm, AddRecordForm
from .models import Record

# Create your views here.
def home(request):
    records = Record.objects.all()

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
        return render(request, 'home.html', {'records': records})


def logout_user(request):
	logout(request)
	messages.success(request, "You Have Been Logged Out...")
	return redirect('home')

def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        
        if form.is_valid():
            form.save()

            # Authenticate and loging
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have been registered')
            return redirect('home')
    else:
        form = SignupForm()
        return render(request, 'register.html', {'form': form})

    return render(request, 'register.html', {'form': form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        # Look up Record
        customer_record = Record.objects.get(id=pk)

        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.error(request, 'You are not allowed to do this')
        return redirect('home')

def delete_customer_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk).delete()
        messages.success(request, "Record deleted successfully")
        return redirect('home')
    else:
        messages.error(request, 'You are not allowed to do this')
        return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)

    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record added successfully!")
                return redirect('home')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.error(request, 'You are not allowed to do this')
        return redirect('home')

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record updated successfully!")
            return redirect('home')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.error(request, 'You are not allowed to do this')
        return redirect('home')