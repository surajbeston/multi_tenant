from django.contrib import admin
from django.urls import path
from .views import home, subscribe, signin, signout, hello_world

urlpatterns = [
    path('', home),
    path('subscribe/', subscribe),
    path('login/', signin),
    path('logout/', signout),
    path('hello-world/', hello_world),
    path('admin/', admin.site.urls),
]
