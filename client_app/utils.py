from django.utils import timezone
import datetime
import pytz
from django_pgschemas.schema import SchemaDescriptor, activate
from django.contrib.auth.models import User

def is_subscribed(request):
    tenant = SchemaDescriptor.create(schema_name="main", domain_url="localhost")
    activate(tenant)

    with tenant:
        user = User.objects.get(username = request.user.username)

        if user.additional.subscription:
            return True        
        else:
            remaining = timezone.now() - user.date_joined
            return remaining < datetime.timedelta(days = 30)
