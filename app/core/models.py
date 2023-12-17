"""
Database models.
"""

from django.db import models
from django.contrib.auth.models import(
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

# Create user manager model
class UserManager(BaseUserManager):
    """Manager for users."""
    # **extra_fields :- provide any number of keyword arguments e.g. name.
    # you can provide number of extra user related info in that.
    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user"""
        if not email:
            raise ValueError("User must have an email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        # supports multiple dbs
        user.save(using=self._db)

        return user

    # for creating super user
    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

# AbstractBaseUser:- for authentication
# PermissionsMixin:- for authorization
class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    # if user can login to django admin
    is_staff = models.BooleanField(default=False)

    # assign UserManager to User class
    objects = UserManager()

    USERNAME_FIELD = "email"



