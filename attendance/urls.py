from rest_framework.routers import DefaultRouter
from django.urls import path, include
from attendance.views import AttendanceViewSet

router = DefaultRouter()
router.register(r'', AttendanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]