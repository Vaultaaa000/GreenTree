from django.db import models


# Create your models here.
from employee.models import Employee


class Performance(models.Model):
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Below Average'),
        (3, '3 - Average'),
        (4, '4 - Good'),
        (5, '5 - Excellent'),
    ]
    review_date = models.DateField()
    rating = models.CharField(max_length=20, choices=RATING_CHOICES)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='performance')

    def __str__(self):
        return f"{self.employee.name} - {self.review_date} - Rating: {self.rating}"

    class Meta:
        db_table = 'performance'
        unique_together = ['employee', 'review_date']
