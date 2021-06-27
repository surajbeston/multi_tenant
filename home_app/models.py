from django.db import models
from django.contrib.auth import get_user_model
from djstripe.models import Customer, Subscription


User = get_user_model()
class Additional(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    subscription = models.ForeignKey(Subscription, null=True, blank=True,on_delete=models.SET_NULL)
