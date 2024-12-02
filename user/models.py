import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from taskmanagement.base import BaseModel

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, first_name=None, last_name=None):
        if not email:
            raise ValueError("User must have email")
        if first_name is not None and last_name is not None:
            user = self.model(
                username=email,
                email=email,
                first_name=first_name,
                last_name=last_name,
            )
        else:
            user = self.model(
                email=email,
            )
        user.save(using=self._db)

        # Create a Client instance linked to the user
        Client.objects.create(user=user, name=f"{user.first_name} {user.last_name}")

        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(
            email,
            first_name,
            last_name,
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True, primary_key=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(
        max_length=100, unique=True, verbose_name="Email")
    mobile = models.CharField(max_length=20, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

class Client(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name