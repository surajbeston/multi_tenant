from django.contrib.auth import authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.db.utils import IntegrityError

from .forms import SignInForm, SignUpForm

from .tenant_utils import create_tenant, send_signup_email


def home(request):
    return HttpResponse(f"Tenant: {request.tenant.schema_name}")

def signup(request):
    form = SignUpForm()
    errors = []
    if request.method == "POST":
        form = SignUpForm(data = request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = User.objects.create_user(data["tenant_name"], data["email"], data["password"])
                user.save()
                redirect_url = create_tenant(data["tenant_name"], data["email"], data["password"])
                send_signup_email(data["email"], data["tenant_name"])
                return redirect(redirect_url)
            except IntegrityError:
                errors.append("Tenant name already used.")
    return render(request, "home_app/signup.html", {"form": form, "errors": errors})

def logout_view(request):
    logout(request)
    return redirect("/")

