from django.db import models
from clients.models import Client
from .enums import JobRole


# Table for jobTypes
class JobTypes(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name}"

# Table for qualificationTypes
class QualificationType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    jobtype = models.ForeignKey(JobTypes, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.jobtype.name}: {self.name}"


# Create your models here.
class Staff(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='staff', null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class StaffJob(models.Model):
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE, related_name='jobs')
    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE, related_name='jobs')
    job = models.ForeignKey(JobTypes, on_delete=models.CASCADE, related_name='staff_jobs')  # FK to JobType


    def __str__(self):
        return f"{self.job} - {self.staff.first_name} {self.staff.last_name} ({self.client.company_name})"

class StaffQualification(models.Model):
    job = models.ForeignKey(StaffJob, on_delete=models.CASCADE, related_name='qualifications')
    qualification = models.ForeignKey(QualificationType, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    passed_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.job.role}) - {self.job.staff.first_name} {self.job.staff.last_name}"
    
    

