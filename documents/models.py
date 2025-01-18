from django.contrib.auth.models import User
from django.db import models
from clients.models import Client
from .enums import  DocumentCategory

# Create your models here.

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
