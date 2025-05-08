from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('hr', 'HR'),
        ('employee', 'Employee'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')
    department = models.ForeignKey('department.Department', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'