from django.contrib import admin
from django.urls import path
from .views import home, signin, signout

urlpatterns = [
    path('', home),
    path('login/', signin),
    path('logout/', signout),
    path('admin/', admin.site.urls),
]
