from django.contrib import admin

# Register your models here.
from department.models import Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'department_name')
    search_fields = ('department_name',)  # 对应search_fields
    ordering = ('department_name',)  # 对应ordering_fields