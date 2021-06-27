from django.conf import settings
import stripe
import djstripe
import json
from djstripe.models import Price
from djstripe import webhooks
from djstripe.models import Subscription, Customer, SubscriptionItem
from stripe.api_resources import subscription

from home_app.models import Additional
from string import punctuation
from django.contrib.auth import authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.db.utils import IntegrityError

from .forms import  SignUpForm

from .tenant_utils import create_tenant, send_signup_email

from pprint import pprint

def home(request):
    return HttpResponse(f"Tenant: {request.tenant.schema_name}")

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
                denied_chars = punctuation[:-6] + punctuation[-5:]
                has_denied_char = False
                for character in data["tenant_name"]:
                    if character in denied_chars:
                        has_denied_char = True
                        break
                if not has_denied_char:
                    user = User.objects.create_user(data["tenant_name"], data["email"], data["password"])
                    user.save()
                    additional = Additional(user = user) 
                    additional.save()
                    redirect_url = create_tenant(data["tenant_name"], data["email"], data["password"])
                    send_signup_email(data["email"], data["tenant_name"])
                    return redirect(redirect_url)
                else:
                    errors.append(f"Only alphabet, numbers and _ allowed in tenant name.")
            except IntegrityError:
                errors.append("Tenant name already used.")
    return render(request, "home_app/signup.html", {"form": form, "errors": errors})

def logout_view(request):
    logout(request)
    return redirect("/")

def create_checkout_session(request):
    stripe.api_key = djstripe.settings.STRIPE_SECRET_KEY
    data =  json.loads(request.body)
    items = data["items"]
    line_items = [{ "price": item["price_id"], "quantity": item["quantity"]} for item in items]

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        customer_email=data["email"],
        line_items=line_items,
        mode='subscription',
        success_url=settings.HOSTNAME + f':8001/{ data["client"] }/',
        cancel_url=settings.HOSTNAME + f':8001/{ data["client"] }/',
    )
    return JsonResponse({
        'id': checkout_session.id
    })

def update_subscription_item(request):
    stripe.api_key = djstripe.settings.STRIPE_SECRET_KEY
    item = json.loads(request.body.decode())
    subscription = stripe.SubscriptionItem.modify(
        item["item_id"],
        quantity = item["quantity"]
    )
    
    # item_obj = SubscriptionItem.objects.get(id = response.id)
    # item_obj.quantity = response["quantity"]
    # item_obj.save()

    SubscriptionItem.sync_from_stripe_data(subscription)
    
    return HttpResponse("done")

def cancel_subscription(request):
    stripe.api_key = djstripe.settings.STRIPE_SECRET_KEY
    subscription_id = json.loads(request.body)["subscription_id"]

    response = stripe.Subscription.delete(subscription_id)
    subscription = Subscription.objects.get(id = response["id"])
    subscription.delete()
    return HttpResponse("done")


@csrf_exempt
def see_item(request):
    stripe.api_key = djstripe.settings.STRIPE_SECRET_KEY
    obj = stripe.SubscriptionItem.retrieve(
        "si_JkSjThUxV5VvJm",
    )
    pprint (obj)
    return JsonResponse(obj)



#STRIPE WEBHOOKS
@webhooks.handler("invoice.payment_succeeded")
def charge_suceeded(event, **kwargs):

    data = event.data["object"]
    email = data["customer_email"]

    try:
        user = User.objects.get(email = email)
        customer = Customer.objects.get(id = data["customer"])
        subscription = Subscription.objects.get(id = data["subscription"])
        user.additional.customer = customer
        user.additional.subscription = subscription
        user.additional.save()
        #can send email from here
    except User.DoesNotExist:
        pass


# @webhooks.handler("charge.succeeded")
# def charge_suceeded(event, **kwargs):
#     pprint (event)
#     pprint (event.__dict__)

# @webhooks.handler("checkout.session.completed")
# def charge_suceeded(event, **kwargs):
#     pprint (event)
#     pprint (event.__dict__)