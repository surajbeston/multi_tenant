from django.contrib import admin
from django.urls import path, include
from .views import home, signup, logout_view, create_checkout_session, update_subscription_item, cancel_subscription, see_item
urlpatterns = [
    path('', home),
    path('signup', signup),
    path('logout', logout_view),
    path('create-checkout-session/', create_checkout_session),
    path('update-subscription-item/', update_subscription_item),
    path('cancel-subscription/', cancel_subscription),
    path('admin/', admin.site.urls),
    path('see/', see_item),
    path("stripe/", include("djstripe.urls", namespace="djstripe")),
]
