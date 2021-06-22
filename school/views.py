from django.http import HttpResponse
from django.contrib.auth import login, logout

from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

from .models import Student
from .forms import SignInForm
from pprint import pprint

def home(request):
    tenant = request.tenant.schema_name
    if request.user.is_authenticated:
        print (request.user)
        print (request.session.items())
        return HttpResponse(tenant)
    else:
        return redirect(f"/{tenant}/login")

def signin(request):
    if request.user.is_anonymous:
        errors=[]
        form = SignInForm()
        if request.method == "POST":
            form = SignInForm(data = request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user = authenticate(username = data["tenant_name"], password = data["password"])
                print (user)
                if user:
                    login(request, user)
                    return redirect(f"/{request.tenant.schema_name}/")
                else:
                    errors.append("Tenant name or password is invalid.")
        return render(request, "school/signin.html", {"form": form, "errors": errors})
    return redirect(f"/{request.tenant.schema_name}/")

@login_required(login_url = "/login")
def signout(request):
    logout(request)
    return redirect("/login")
