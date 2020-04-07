from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

from pages.helpers import validate_email
from pages.models import Patient


def show_signup(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect('/info/')
        return render(request, 'accounts/patient/signup.html')
    elif request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not validate_email(email):
            return render(request, 'accounts/patient/signup.html', {'error_message': 'Invalid email address entered.'})
        user_exists = User.objects.filter(username=email).exists()
        if user_exists:
            return render(request, 'accounts/patient/signup.html', {'error_message': 'User already exists.'})
        user = User(email=email, first_name=first_name, last_name=last_name, username=email)
        user.set_password(password)
        user.save()
        patient = Patient(user=user)
        patient.save()
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/info/')
        else:
            """redirect to login"""
            return HttpResponseRedirect('/account/login/')


def show_login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect('/info/')
        return render(request, 'accounts/patient/login.html', {})
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/info/')
        else:
            """return invalid login here"""
            return render(request, 'accounts/patient/login.html', {'error_message': 'Wrong username or password.'})


def show_logout(request):
    if request.method == 'GET':
        logout(request)
        return HttpResponseRedirect('/')


@login_required(login_url='/accounts/login/')
def show_medical_info(request):
    return render(request, 'pages/medinfo.html')
