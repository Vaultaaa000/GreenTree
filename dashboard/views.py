from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count
from datetime import datetime, timedelta
from department.models import Department
from employee.models import Employee
from attendance.models import Attendance
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


def dashboard_view(request):
    """dashboard home page"""
    return render(request, 'dashboard/index.html')


@api_view(['GET'])
@permission_classes([AllowAny])
def department_data(request):
    """API endpoint: Returns department employee distribution data"""
    # 使用 annotate 获取每个部门的员工数量
    departments = Department.objects.annotate(employee_count=Count('employee'))
    department_names = [dept.department_name for dept in departments]
    employee_counts = [dept.employee_count for dept in departments]

    return JsonResponse({
        'department_names': department_names,
        'employee_counts': employee_counts
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def attendance_data(request):
    """API endpoint: Returns attendance statistics for the past 30 days"""
    # 获取过去30天的日期
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)

    # 获取日期范围内的所有日期
    days = []
    current_date = start_date
    while current_date <= end_date:
        days.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)

    # 初始化数据结构
    present_counts = [0] * len(days)
    late_counts = [0] * len(days)
    absent_counts = [0] * len(days)

    # 查询出勤数据
    attendance_records = Attendance.objects.filter(date__range=[start_date, end_date])

    # 分组统计各状态的员工数量
    for i, day in enumerate(days):
        day_date = datetime.strptime(day, '%Y-%m-%d').date()
        day_records = attendance_records.filter(date=day_date)

        present_counts[i] = day_records.filter(status='present').count()
        late_counts[i] = day_records.filter(status='late').count()
        absent_counts[i] = day_records.filter(status='absent').count()

    return JsonResponse({
        'days': days,
        'present_counts': present_counts,
        'late_counts': late_counts,
        'absent_counts': absent_counts
    })
