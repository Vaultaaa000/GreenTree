from rest_framework import serializers

# from api.models import UserProfile
from employee.models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    department_name = serializers.ReadOnlyField(source='department.department_name')

    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'phone', 'address', 'join_date', 'department', 'department_name']




