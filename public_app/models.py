import uuid
from django.db import models
from django.db.models.deletion import CASCADE
from djstripe.models import Customer, Subscription
from django.contrib.auth.models import User, AbstractUser
from django_pgschemas.models import TenantMixin, DomainMixin

class Client(TenantMixin):
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)

class Domain(DomainMixin):
    pass

