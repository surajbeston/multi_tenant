from django.contrib import admin
from django.urls import path
from .views import home, signup, logout_view

urlpatterns = [
    path('', home),
    path('signup', signup),
    path('logout', logout_view),
    path('admin/', admin.site.urls),
]
