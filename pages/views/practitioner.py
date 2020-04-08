from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

from pages.helpers import validate_email
from pages.models import Practitioner, Illness, MedicalInfo, Patient


def signup_page(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect('/dashboard/')
        return render(request, 'accounts/practitioner/signup.html')
    elif request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not validate_email(email):
            return render(request, 'accounts/practitioner/signup.html',
                          {'error_message': 'Invalid email address entered.'})
        user_exists = User.objects.filter(username=email).exists()
        if user_exists:
            return render(request, 'accounts/practitioner/signup.html', {'error_message': 'User already exists.'})
        user = User(email=email, first_name=first_name, last_name=last_name, username=email)
        user.set_password(password)
        user.save()
        practitioner = Practitioner(user=user)
        practitioner.save()
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/dashboard/')
        else:
            """redirect to login"""
            return HttpResponseRedirect('/account/p/login/')


def login_page(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect('/dashboard/')
        return render(request, 'accounts/practitioner/login.html', {})
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/dashboard/')
        else:
            """return invalid login here"""
            return render(request, 'accounts/practitioner/login.html', {'error_message': 'Wrong username or password.'})


def logout_page(request):
    if request.method == 'GET':
        logout(request)
        return HttpResponseRedirect('/')


def is_valid_queryparam(param):
    return param != '' and param is not None


def filter(request):
    qs = MedicalInfo.objects.all()
    illnesses = Illness.objects.all()
    patients = Patient.objects.all()
    summary_contains_query = request.GET.get('summary_contains')
    exact_blood_type = request.GET.get('blood_type')
    exact_gender = request.GET.get('exact_gender')
    age_min = request.GET.get('age_min')
    age_max = request.GET.get('age_max')
    illness = request.GET.get('illness')

    if is_valid_queryparam(summary_contains_query):
        qs = qs.filter(summary__icontains=summary_contains_query)

    if is_valid_queryparam(age_min):
        qs = qs.filter(age__gte=age_min)

    if is_valid_queryparam(age_max):
        qs = qs.filter(age__lt=age_max)

    if is_valid_queryparam(exact_blood_type):
        qs = qs.filter(blood_group=exact_blood_type)

    if is_valid_queryparam(exact_gender):
        qs = qs.filter(gender=exact_gender)

    if is_valid_queryparam(illness) and illness != 'Choose...':
        qs = qs.filter(illnesses__name=illness)

    return qs


@login_required(login_url='/accounts/p/login/')
def show_doc_info(request):
    if request.method == "GET":
        qs = filter(request)
        context = {
            'queryset': qs,
            'illnesses': Illness.objects.all(),
        }
        return render(request, "pages/dashboard.html", context)
