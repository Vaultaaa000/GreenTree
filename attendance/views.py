from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.
from attendance.models import Attendance
from attendance.serializers import AttendanceSerializer
from accounts.permissions import IsHR, IsOwnerOrHRAdmin


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['employee', 'date', 'status']
    ordering_fields = ['date', 'employee__name']

    def get_queryset(self):
        """
        Employees can only see their own attendance records
        """
        queryset = Attendance.objects.all()
        user = self.request.user

        if user.is_superuser:
            return queryset

        if not hasattr(user, 'role'):
            return Attendance.objects.none()

        if user.role == 'employee':
            try:
                employee = user.employee_profile
                return queryset.filter(employee=employee)
            except:
                if hasattr(user, 'email'):
                    return queryset.filter(employee__email=user.email)
                return Attendance.objects.none()

        return queryset
