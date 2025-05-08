from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.
from rest_framework.permissions import IsAuthenticated

from performance.models import Performance
from performance.serializers import PerformanceSerializer
from accounts.permissions import IsHR, IsOwnerOrHRAdmin


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['employee', 'review_date', 'rating']
    ordering_fields = ['review_date']

    def get_permissions(self):
        """
        根据操作分配权限：
        - 创建、更新和删除：只有HR可以操作
        - 列表和检索：员工可以看自己的信息，HR可以看所有人
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsHR]
        else:
            permission_classes = [IsOwnerOrHRAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        重写查询集方法，员工只能看到自己的绩效记录
        """
        queryset = Performance.objects.all()
        user = self.request.user

        # 如果是superuser，返回所有记录
        if user.is_superuser:
            return queryset

        # 如果用户没有role属性，默认为不能查看任何记录
        if not hasattr(user, 'role'):
            return Performance.objects.none()

        # 如果是普通员工，只能看到自己的绩效
        if user.role == 'employee':
            # 先尝试通过用户关联获取员工，再查询绩效
            try:
                employee = user.employee_profile
                return queryset.filter(employee=employee)
            except:
                # 如果关联不存在，尝试通过邮箱匹配
                if hasattr(user, 'email'):
                    return queryset.filter(employee__email=user.email)
                return Performance.objects.none()

        # HR和Admin可以看到所有记录
        return queryset