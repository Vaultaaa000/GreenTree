# dashboard/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('api/dashboard/department-data/', views.department_data, name='department_data'),
    path('api/dashboard/attendance-data/', views.attendance_data, name='attendance_data'),
]