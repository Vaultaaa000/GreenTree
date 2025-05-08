from django.shortcuts import render

from accounts.permissions import IsEmployee, IsHR
from department.models import Department
from department.serializers import DepartmentSerializer
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['department_name']
    ordering_fields = ['department_name']

    def get_permissions(self):
        """
        Assign permissions based on operations:
        - List and retrieve: All authenticated users can access
        - Create, update and delete: Only HR and Admin can access
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsEmployee]
        else:
            permission_classes = [IsHR]
        return [permission() for permission in permission_classes]