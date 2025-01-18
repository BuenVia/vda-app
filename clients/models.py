from django.contrib.auth.models import User
from django.db import models


class Client(models.Model):
    company_name = models.CharField(max_length=255, unique=True)
    address_line_1 = models.CharField(max_length=255, blank=True, null=True)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    town = models.CharField(max_length=100, blank=True, null=True)
    county = models.CharField(max_length=100, blank=True, null=True)
    postcode = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.company_name

User.add_to_class('client', models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=False))