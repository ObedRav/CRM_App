#!/usr/bin/python3
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignupForm, AddRecordForm
from .models import Record


# Create your views here.
def home(request):
    """
    This function is responsible for displaying the home page of the CRM application.
    It retrieves all the records from the Record model and passes them to the home.html template to be rendered.
    If the request method is POST, it means the user is trying to log in.
    The user's provided username and password are authenticated and if successful, the user is logged in and a success message is displayed.
    If the authentication fails, an error message is displayed.
    If the authentication is not being attempted, the home.html template is rendered with the retrieved records.
    """
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
    """
    This function logs out the currently logged-in user and redirects them to the home page.
    A success message is displayed to inform the user that they have been logged out.
    """
    logout(request)
    messages.success(request, "You Have Been Logged Out...")
    return redirect('home')


def register(request):
    """
    This function is responsible for handling user registration.
    If the request method is POST, it means the user is submitting a registration form.
    The SignupForm is validated and if it is valid, the user is registered and logged in.
    A success message is displayed to inform the user that they have been registered.
    If the form is not valid or if the request method is not POST, the register.html template is rendered with the SignupForm.
    """
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
    """
    This function displays the details of a specific customer record.
    If the user is authenticated, it retrieves the record with the provided primary key (pk) from the Record model and passes it to the record.html template to be rendered.
    If the user is not authenticated, an error message is displayed and the user is redirected to the home page.
    """
    if request.user.is_authenticated:
        # Look up Record
        try:
            customer_record = Record.objects.get(id=pk)
        except:
            messages.error(request, 'The user doesn\'t exist')
            return render(request, 'base.html')

        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.error(request, 'You are not allowed to do this')
        return redirect('home')


def delete_customer_record(request, pk):
    """
    This function deletes a specific customer record.
    If the user is authenticated, it retrieves the record with the provided primary key (pk) from the Record model and deletes it.
    A success message is displayed to inform the user that the record has been deleted.
    If the user is not authenticated, an error message is displayed and the user is redirected to the home page.
    """
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk).delete()
        messages.success(request, "Record deleted successfully")
        return redirect('home')
    else:
        messages.error(request, 'You are not allowed to do this')
        return redirect('home')


def add_record(request):
    """
    This function is responsible for handling the addition of a new customer record.
    If the user is authenticated, it renders the add_record.html template with the AddRecordForm.
    If the request method is POST, the form is validated and if it is valid, a new record is added to the Record model.
    A success message is displayed to inform the user that the record has been added.
    If the user is not authenticated, an error message is displayed and the user is redirected to the home page.
    """
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
    """
    This function is responsible for handling the updating of an existing customer record.
    If the user is authenticated, it retrieves the record with the provided primary key (pk) from the Record model and passes it to the update_record.html template to be rendered with the AddRecordForm.
    If the request method is POST, the form is validated and if it is valid, the existing record is updated.
    A success message is displayed to inform the user that the record has been updated.
    If the user is not authenticated, an error message is displayed and the user is redirected to the home page.
    """
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record updated successfully!")
            return redirect('home')
        return render(request, 'update_record.html', {'form': form, 'current_record': current_record})
    else:
        messages.error(request, 'You are not allowed to do this')
        return redirect('home')
