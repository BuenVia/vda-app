from django.db import models
from clients.models import Client

# Create your models here.
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