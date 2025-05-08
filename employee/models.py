from django.db import models

# Create your models here.
from department.models import Department
from djangoAssessment import settings


class Employee(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    address = models.TextField(max_length=255)
    join_date = models.DateField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                                related_name='employee_profile')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'employee'





