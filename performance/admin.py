from django.contrib import admin

# Register your models here.
from performance.models import Performance


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'review_date', 'rating')
    list_filter = ('employee', 'review_date', 'rating')  # 对应filterset_fields
    search_fields = ('employee__name',)  # 允许通过员工名称搜索
    ordering = ('review_date',)  # 对应ordering_fields
    date_hierarchy = 'review_date'  # 增强日期过滤功能