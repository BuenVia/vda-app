from django.db import models
from clients.models import Client
from .enums import JobRole

# Create your models here.
class Staff(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='staff', null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Job(models.Model):
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE, related_name='jobs')
    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE, related_name='jobs')
    role = models.CharField(
        max_length=3,
        choices=[(role.name, role.value) for role in JobRole]
    )

    def __str__(self):
        return f"{self.role} - {self.staff.first_name} {self.staff.last_name} ({self.client.company_name})"

class Qualification(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='qualifications')
    name = models.CharField(max_length=255)
    passed_date = models.DateField()
    expiry_date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.job.role}) - {self.job.staff.first_name} {self.job.staff.last_name}"