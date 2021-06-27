# Django Multi Tenant

Setting up project for development
-------------------------------------------

### Setting Up Enviroment

(__Move into project directory.__)

1. python3 -m venv venv
2. source venv/bin/activate
3. pip install -r requirements.txt

## Setting up settings.py

1. Configure email server from line 149 of settings.py.

* You'll need your SMTP server address.
* You'll need email address and password.
* I was using gmail for testing, whose SMTP is configured and you'll need to add you gmail credentials.

2. Configure stripe config from line 188
* You'll need to get PUBLIC_KEY and SECRET_KEY from stripe dashboard and use here.
* Install `stripe cli` and use `stripe listen --forward-to localhost:8000/stripe/webhook/` to listen to webhooks which update database upon any change.


### Setting up database
1. python manage.py migrate -s public
2. python manage.py migrate
3. python manage.py createsuperuser (create superuser)
4. python manage.py runschema djstripe_sync_plans_from_stripe
* Insert `main` when pompt is presented to select tenant.

Using project
------------------------
  (__Run development server__)
