# Register your models here.
from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'address', 'join_date', 'department')
    list_filter = ('department', 'join_date')  # 对应filterset_fields
    search_fields = ('name', 'email')  # 对应search_fields
    ordering = ('name', 'join_date', 'department__department_name')  # 对应ordering_fields
