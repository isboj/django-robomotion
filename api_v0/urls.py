from django.conf.urls import url
from django.urls import path

from rest_framework import routers
from .views import RobotViewSet, MotionViewSet, ValueViewSet
from .views import RobotValueListAPIView, ShareRobotValueListAPIView, ValueSetView

router = routers.DefaultRouter()
router.register('robots', RobotViewSet)
router.register('motions', MotionViewSet)
router.register('values', ValueViewSet)

urlpatterns = [
    path('robot_values/<int:robot_id>/', RobotValueListAPIView.as_view(), name="robot_values"),
    path('share_key/<str:share_key>', ShareRobotValueListAPIView.as_view(), name="share_key_values"),
    path('value_set/<str:robot_name>/<str:motion_name>', ValueSetView.as_view(), name="set_value")
]

urlpatterns += router.urls
