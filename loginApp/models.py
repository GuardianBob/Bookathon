from django.db import models
import re, datetime
import bcrypt

class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    user_type = models.TextField(blank=True) # null=True
    user_level = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Address(models.Model):
    number = models.IntegerField()
    street = models.CharField(max_length=100)
    street2 = models.CharField(max_length=100, blank=True)
    apt_num = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=10)
    zipcode = models.IntegerField()
    user = models.ForeignKey(User, related_name='user_address', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    @property
    def street_address(self):
        return f"{self.number} {self.street} {self.street2} {self.apt}"
