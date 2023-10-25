from django.db import IntegrityError
from django.contrib.auth.models import User

from dotenv import load_dotenv
import os

load_dotenv()

username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'root')
email = os.getenv('DJANGO_SUPERUSER_EMAIL', default="test@mail.com")
password = os.getenv('DJANGO_SUPERUSER_PASSWORD', default="Asd4567890")

try:
    superuser = User.objects.create_superuser(
        username=username,
        email=email,
        password=password)
    superuser.save()
except IntegrityError:
    print(f"Super User with username {username} is already exit!")
except Exception as e:
    print(e)