from django.db import models

# Create your models here.
from employee.models import Employee


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    ]
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')

    def __str__(self):
        return f"{self.employee.name}--{self.date}--{self.status}"

    class Meta:
        db_table = 'attendance'
        unique_together = ['employee', 'date']