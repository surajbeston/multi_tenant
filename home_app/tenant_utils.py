from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth import login
from django.contrib.auth.models import User
from django_pgschemas.utils import get_domain_model
from django_pgschemas.schema import activate

from public_app.models import Client, Domain

def create_tenant(tenant_name, email, password):
    client = Client.objects.create(schema_name=tenant_name)
    Domain.objects.create(domain="localhost", folder=tenant_name, tenant=client) #change domain name
    return create_tenant_user(tenant_name, email, password)

def create_tenant_user(tenant_name, email, password):
    #GETTING TENANT AND ACTIVATING IT TO CREATE UNDER IT
    DomainModel = get_domain_model()
    domain = DomainModel.objects.select_related("tenant").get(domain=settings.HOSTNAME.split("://")[1], folder=tenant_name)
    tenant = domain.tenant
    activate(tenant)

    with tenant:
        user = User.objects.create(username = tenant_name, email = email, is_staff = True, is_superuser = True)
        user.set_password(password)
        user.save()

    return f"/{tenant_name}/login/"

def send_signup_email(email, tenant_name):
    url = f"{settings.HOSTNAME}/{tenant_name}/login"
    send_mail(
        subject = 'Tenant successfully created.',
        message = f'Your tenant has been successfully created. Please login here with required credentials: {url}  ',
        from_email = 'getsurajjha@gmail.com',
        recipient_list = [email],
        fail_silently=True,
    )    
