from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from .models import Job, Application

def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "portal/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome, {user.username}!")
            return redirect("job_list")
        else:
            messages.error(request, "Invalid credentials")
            return redirect("login")
    return render(request, "portal/login.html")

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")

@login_required
def job_list(request):
    jobs = Job.objects.all()
    return render(request, "portal/job_list.html", {"jobs": jobs})

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    Application.objects.get_or_create(job=job, applicant=request.user)
    messages.success(request, f"You applied for {job.title}")
    return redirect("job_list")
