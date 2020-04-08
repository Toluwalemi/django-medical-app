from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

from pages.helpers import validate_email
from pages.models import Patient, MedicalInfo, Illness


def show_signup(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect('/report/')
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
            return HttpResponseRedirect('/report/')
        else:
            """redirect to login"""
            return HttpResponseRedirect('/account/login/')


def show_login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect('/report/')
        return render(request, 'accounts/patient/login.html', {})
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/report/')
        else:
            """return invalid login here"""
            return render(request, 'accounts/patient/login.html', {'error_message': 'Wrong username or password.'})


def show_logout(request):
    if request.method == 'GET':
        logout(request)
        return HttpResponseRedirect('/')


@login_required(login_url='/accounts/login/')
def patient_create_view(request, illnesses=Illness.objects.all()):
    if request.method == 'GET':
        # patients = Patient.objects.filter(patient__id=request.user.id)
        # illnesses = Illness.objects.all()
        c = {
            # 'patients': patients,
            'illnesses': illnesses
        }
        return render(request, 'pages/report.html', c)
    elif request.method == "POST":
        summary = request.POST.get('summary')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        blood_group = request.POST.get('blood_group')
        illness = request.POST.get('illness')
        # some_stuff = Illness(illnesses__name=illness)
        report_info = MedicalInfo.objects.create(patient_id=request.user.id,
                                                 summary=summary, gender=gender, age=age,
                                                 blood_group=blood_group)
        # report_info.save()
        # report_info.illnesses.add(illness)
        return HttpResponseRedirect('/stat/')
