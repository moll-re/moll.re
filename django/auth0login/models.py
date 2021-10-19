from types import resolve_bases
from django.db import models

# Create your models here.
def set_roles(backend, user, response, *args, **kwargs):
    if backend.name == 'auth0':
        if user.email == "me@moll.re":
            user.is_staff = True
            user.is_admin = True
            user.is_superuser = True
            user.save()

