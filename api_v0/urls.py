from django.conf.urls import url
from django.urls import path

from rest_framework import routers
from .views import RobotViewSet, MotionViewSet, ValueViewSet
from .views import RobotValueListAPIView

router = routers.DefaultRouter()
router.register('robots', RobotViewSet)
router.register('motions', MotionViewSet)
router.register('values', ValueViewSet)

urlpatterns = [
    path('robot_values/<int:robot_id>/', RobotValueListAPIView.as_view(), name="robot_values"),
]

urlpatterns += router.urls
