import datetime
import os

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django import forms
from . import forms
from django.shortcuts import render

from .models import Course, School, Reservation
from .forms import LoginForm, RegisterForm



# Create your views here.

# Main page view
def index(request):
    schools = School.objects.all()
    icons = {
        1: 'fas fa-square',
        2: 'fas fa-th-large',
        3: 'fas fa-th',
        4: 'fas fa-th',
        5: 'fas fa-th',
    }
    return render(request, 'templates/school_list.html', {'schools': schools, 'icons': icons})

# Create course page view
def create_course(request):
    if request.method == 'POST':
        form = forms.CourseCreationForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Course created successfully!")
            return redirect('index')
    else:
        form = forms.CourseCreationForm(user=request.user)

    return render(request, 'templates/create_course.html', {'form': form})

# Reservation page view
def reservations_pages(request):
    user = request.user
    user_groups = user.groups.all()
    reservations = Reservation.objects.none()

    if user.is_authenticated:
        if user_groups.filter(name='schools').exists():
            school = School.objects.get(name=user.username)
            reservations = Reservation.objects.filter(school=school).select_related('course')
        else:
            reservations = Reservation.objects.filter(user=user).select_related('course')

        if request.method == 'POST':
            booking = Reservation.objects.filter(id=request.POST.get("id"))
            booking.delete()
            messages.success(request, "Votre annulation a été prise en compte!")
            return redirect("Reservations")

    return render(request, 'templates/reservations.html', {'reservations': reservations})


def courses_list(request, school_name):
    icons = {
        1: 'fas fa-square',
        2: 'fas fa-th-large',
        3: 'fas fa-th',
        4: 'fas fa-th',
        5: 'fas fa-th',
    }
    school = School.objects.get(name=school_name)
    courses = Course.objects.filter(school=school)

    # Générer tous les jours de la semaine sans vérifier la validité
    weekdays = [(datetime.datetime.now() + datetime.timedelta(days=i)).strftime("%A") for i in range(7)]

    # Utiliser tous les créneaux horaires sans vérifier la validité
    time = ["8h", "9h", "10h", "11h", "14h", "15h", "16h", "17h"]

    slots = []
    for day in weekdays:
        slots.append({
            "day": day,
            'time': time
        })

    if request.method == 'POST':
        course_id = request.POST.get("course_id")
        course = Course.objects.get(id=course_id)
        booking = Reservation.objects.create(
            user=request.user,
            school=school,
            course=course,
            time=request.POST.get("time"),
            date=request.POST.get("day"),
        )
        booking.save()
        messages.success(request, "Votre réservation a été prise en compte!")
        return redirect("Reservations")
    else:
        return render(request, 'templates/courses_list.html',
                  {'school_name': school_name, 'weekdays': weekdays, 'times': time, 'slots': slots, 'courses': courses, 'icons': icons})

def login_register_page(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == 'POST':
        # If the user is trying to login
        if 'login_form' in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                user = authenticate(username=login_form.cleaned_data['username'], password=login_form.cleaned_data['password'])
                if user is not None:
                    login(request, user)
                    messages.success(request, f"Bonjour {user.username}, vous êtes connecté !")
                    return redirect('index')
                else:
                    messages.info(request, f"Echec de la connexion")

        # If the user is trying to register
        elif 'register_form' in request.POST:
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                register_form.save()
                username = register_form.cleaned_data['username']
                password = register_form.cleaned_data['password1']
                user = authenticate(username=username, password=password)
                login(request, user)
                messages.success(request, "Votre compte a été créé !")
                return redirect('index')

    # If the request is GET
    else:
        login_form = LoginForm()
        register_form = RegisterForm()

    return render(request, 'templates/login_register.html', {'login_form': login_form, 'register_form': register_form})

# Logout view
@login_required
def logout_page(request):
    logout(request)
    messages.info(request, "Vous êtes déconnecté.")
    return redirect("index")
