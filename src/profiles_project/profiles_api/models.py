from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

from PIL import Image
import os

# Create your models here.

class UserProfileManager(BaseUserManager):
    """ Helps DJango work with our custom user model"""

    def create_user(self,email,name,password=None):
        """ Create a new user profile object"""
        if not email:
            raise ValueError('Users must have an email adress.')
        email = self.normalize_email(email)
        user = self.model(email=email,name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,email, name, password):
        """ Creates and saves a new superuser with given details"""
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """ Represents a "user profile inside our system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    url_image = models.CharField(max_length=100, null=True)
    url_docs = models.CharField(max_length=500, null=True)
    plan_id = models.IntegerField(default=1)
    status = models.IntegerField(default=1)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','lastname','phone']

    def get_full_name(self):
        """Used to get a full name"""
        return self.name + self.lastname

    def get_short_name(self):
        """ Used to get a short name"""
        return self.name

    def __str__(self):
        """ Used for Django to convert object to String"""
        return self.email

class UserProcessHistory(models.Model):
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    description = models.CharField(max_length=500, null=True)
    last_mod = models.DateTimeField(auto_now_add=True)
    full_storage = models.DecimalField(max_digits=20, decimal_places=4,default=0)
    filled_storage = models.DecimalField(max_digits=20, decimal_places=4,default=0)
    filled_storage_doc = models.DecimalField(max_digits=20, decimal_places=4,default=0)
    filled_storage_music = models.DecimalField(max_digits=20, decimal_places=4,default=0)
    filled_storage_video = models.DecimalField(max_digits=20, decimal_places=4,default=0)
    filled_storage_image = models.DecimalField(max_digits=20, decimal_places=4,default=0)
    status = models.IntegerField(default=1)

class ProfileFeedItem(models.Model):
    """Profile status update."""
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the model as a string"""
        return self.status_text

class Image(models.Model):
    """Image model"""
    detail = models.CharField(max_length=255, default="Nombre")
    image = models.ImageField("images")

    def __str__(self):
        """Used for Django to convert object to String"""
        return self.detail

class AnyFile(models.Model):
    """File model"""
    detail = models.CharField(max_length=255, default="Nombre")
    anyfile = models.FileField("anyfile")

    def __str__(self):
        """Used for Django to convert object to String"""
        return self.detail

class Filetype(models.Model):
    """Tipos de archivo"""
    name = models.CharField(max_length=255, default="Nombre")
    status = models.IntegerField(default=1)

    def __str__(self):
        """Used for Django to convert object to String"""
        return self.name

""" To get the file url"""
def magic_url(instance, filename):
    print(instance.filename)
    return os.path.join( instance.url_docs + "/" + instance.filename)

class UserFile(models.Model):
    """Los archivos de los usuarios"""
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    email = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    filesize = models.CharField(max_length=255)
    filetype = models.ForeignKey('Filetype', on_delete=models.CASCADE)
    url_docs = models.CharField(max_length=255)
    last_mod = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)
    detail = models.CharField(max_length=255)
    anyfile = models.FileField("anyfile",upload_to=magic_url)

    def __str__(self):
        """Used for Django to convert object to String"""
        return self.filename

class UserPlan(models.Model):
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    plan = models.ForeignKey('PlanType', on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)

class PlanType(models.Model):
    name = models.CharField(max_length=255, default="")
    price = models.DecimalField(max_digits=20, decimal_places=4,default=0)
    storage = models.DecimalField(max_digits=20, decimal_places=4,default=0)
    detail = models.CharField(max_length=255, default="")
    status = models.IntegerField(default=1)

    def __str__(self):
        """ Used for Django to convert object to String"""
        return str(self.id)

class status(models.Model):
    name = models.CharField(max_length=255, default="")

    def __str__(self):
        """ Used for Django to convert object to String"""
        return str(self.name)
