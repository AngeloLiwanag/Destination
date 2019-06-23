from __future__ import unicode_literals
from django.db import models
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len (postData['fname']) < 2:
            errors['fname'] = 'first name should be at least 2 characters'
        if len (postData['lname']) < 2:
            errors['lname'] = 'Last name should be at least 2 characters'
            print (errors['lname'])
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Email is not valid'
        if len(postData['password']) < 8:
            errors['network'] = 'Password should be at least 8 characters'
        return errors

    def log_validator(self, postData):
        errors = {}
        if not EMAIL_REGEX.match(postData['email']): #TEST QUESTION 
            errors['email'] = 'Login email is not valid'
        if len(postData['password']) < 8:
            errors['network'] = 'Login password should be at least 8 characters'
        # print(errors)
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class TripsManager(models.Manager):
    def create_validator(self, postData):
        errors = {}
        if len (postData['destination']) < 3:
            errors['destination'] = 'A trip destination must consist of at least 3 characters'
        if len (postData['start_date']) < 8:
            errors['start_date'] = "A start date must be provided"
        if len (postData['end_date']) < 8:
            errors['end_date'] = "A end date must be provided"
        if len (postData['plan']) < 1:
            errors['plan'] = 'A plan must be provided!'
        return errors
    def update_validator(self, postData):
        errors = {}
        if len (postData['destination']) < 3:
            errors['destination'] = 'A trip destination must consist of at least 3 characters'
        if len (postData['plan']) < 1:
            errors['plan'] = 'A plan must be provided!'
        return errors

class Trips(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.CharField(max_length=255)
    end_date = models.CharField(max_length=255)
    plan = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="trips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripsManager()
    # Create your models here.
