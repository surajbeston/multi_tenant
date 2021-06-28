from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import login, logout

from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

from .forms import SignInForm
from pprint import pprint

from django_pgschemas.schema import SchemaDescriptor, activate
from .utils import is_subscribed #use this to check the trial

def home(request):
    tenant_name = request.tenant.schema_name
    if request.user.is_authenticated:
        if is_subscribed(request):
            return redirect(f"/{tenant_name}/hello-world")
        else:
            return redirect(f"/{tenant_name}/subscribe")
    else:
        return redirect(f"/{tenant_name}/login")

def hello_world(request):
    tenant_name = request.tenant.schema_name
    if request.user.is_authenticated:
        if is_subscribed(request):
            return HttpResponse("Hello world! You're seeing this because you're either subscribed or have trial remaining.")
    return redirect(f"/{tenant_name}/")


def subscribe(request):
    tenant_name = request.tenant.schema_name
    if request.user.is_authenticated:
        tenant = SchemaDescriptor.create(schema_name="main", domain_url="localhost")
        activate(tenant)

        with tenant:
            import djstripe
            from djstripe.models import Product, Price, SubscriptionItem

            # products = Product.objects.all()
            # active_products = [product for product in products if product.active]
            user = User.objects.get(username = tenant_name)

            if user.additional.subscription:
                pprint(user.additional.subscription.__dict__)
                items = SubscriptionItem.objects.filter(subscription = user.additional.subscription)
                subs_items = []
                for item in items:
                    price = Price.objects.get(pk = item.price_id)
                    subs_items.append({"price": price, "item": item})
                context = {"items": subs_items}
            else:
                
                basepackage_price = Price.objects.get(product__name = "basepackage")

                email_price = Price.objects.get(product__name = "email")

                task_price = Price.objects.get(product__name = "task")

                context =  {"prices": {"basepackage_price": basepackage_price, "email_price": email_price, "task_price": task_price}}

        return render(request, "client_app/subscribe.html", {"user": request.user, "tenant_name": tenant_name, **context})
    else:
        return redirect(f"/{tenant_name}/login")



def signin(request):
    if request.user.is_anonymous:
        errors=[]
        form = SignInForm()
        if request.method == "POST":
            form = SignInForm(data = request.POST)
            if form.is_valid():
                data = form.cleaned_data
                try:
                    email_user = User.objects.get(email = data["email"])
                    user = authenticate(username = email_user.username, password = data["password"])
                    if user:
                        login(request, user)
                        return redirect(f"/{request.tenant.schema_name}/")
                    else:
                        errors.append("Email or password is invalid.")
                except User.DoesNotExist:
                    errors.append("Email or password incorrect.")
        return render(request, "client_app/signin.html", {"form": form, "errors": errors})
    return redirect(f"/{request.tenant.schema_name}/")

@login_required(login_url = "/login")
def signout(request):
    logout(request)
    return redirect("/login")

