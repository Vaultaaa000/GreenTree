from django.db import models


# Create your models here.
class Department(models.Model):
    department_name = models.CharField()

    def __str__(self):
        return self.department_name

    class Meta:
        db_table = 'department'
