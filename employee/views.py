from django.shortcuts import render
# Create your views here.

from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from accounts.permissions import IsOwnerOrHRAdmin, IsHR, IsAdmin
from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department', 'join_date']
    search_fields = ['name', 'email']
    ordering_fields = ['name', 'join_date', 'department__department_name']

    def get_permissions(self):
        """
        根据操作分配权限：
        - 列表：HR和Admin可以访问所有员工
        - 检索：员工可以看自己的信息，HR和Admin可以看所有人
        - 创建、更新和删除：只有HR和Admin可以操作
        """
        if self.action == 'list':
            permission_classes = [IsHR]
        elif self.action == 'retrieve':
            permission_classes = [IsOwnerOrHRAdmin]
        else:
            permission_classes = [IsHR]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        重写查询集方法，员工只能看到自己的记录
        """
        queryset = Employee.objects.all()
        user = self.request.user

        # 如果是superuser，返回所有记录
        if user.is_superuser:
            return queryset

        # 如果用户没有role属性，默认为不能查看任何记录
        if not hasattr(user, 'role'):
            return Employee.objects.none()

        # 如果是普通员工，只能看到与自己关联的记录
        if user.role == 'employee':
            # 尝试通过user字段关联查找
            employee_queryset = queryset.filter(user=user)

            # 如果没有找到，尝试通过email查找
            if not employee_queryset.exists() and hasattr(user, 'email'):
                employee_queryset = queryset.filter(email=user.email)

            return employee_queryset

        # HR和Admin可以看到所有记录
        return queryset

