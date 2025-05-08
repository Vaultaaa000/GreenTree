from rest_framework import serializers

from performance.models import Performance


class PerformanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.ReadOnlyField(source='employee.name')

    class Meta:
        model = Performance
        fields = ['id', 'review_date', 'rating', 'employee', 'employee_name']