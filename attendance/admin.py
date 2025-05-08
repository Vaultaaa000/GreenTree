from django.contrib import admin

# Register your models here.
from attendance.models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'date', 'status')
    list_filter = ('employee', 'date', 'status')  # 对应filterset_fields
    search_fields = ('employee__name',)  # 允许通过员工名称搜索
    ordering = ('date', 'employee__name')  # 对应ordering_fields
    date_hierarchy = 'date'  # 增强日期过滤功能
