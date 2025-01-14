from django.contrib.auth.models import User
from django.db import models
from .enums import JobRole, DocumentCategory

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

# User.add_to_class('client', models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=False))

class Staff(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='staff', null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Job(models.Model):
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE, related_name='jobs')
    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='jobs')
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


class ToolEquipment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='tools_equipment')
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.client.company_name})"


class CalibrationTest(models.Model):
    equipment = models.ForeignKey(ToolEquipment, on_delete=models.CASCADE, related_name='tests')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='tests')
    test_name = models.CharField(max_length=255)
    test_completion_date = models.DateField()
    test_renewal_date = models.DateField()
    test_score = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.test_name} ({self.equipment.make} {self.equipment.model})"


class Document(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='documents')
    category = models.CharField(
        max_length=50,
        choices=[(category.name, category.value) for category in DocumentCategory],
        unique=True
    )
    file = models.FileField(upload_to='uploads/documents/', blank=True, null=True)
    upload_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_category_display()} - {self.client.company_name}"

    def save(self, *args, **kwargs):
        if self.file:
            # Rename the file
            import os
            from django.utils.text import slugify
            client_name = slugify(self.client.company_name)
            category_name = slugify(self.get_category_display())
            extension = os.path.splitext(self.file.name)[1]
            self.file.name = f"{category_name}_{client_name}_{self.client.id}{extension}"
        super().save(*args, **kwargs)
