from django.urls import path

from rest_framework import routers
from .views import RobotViewSet, MotionViewSet, ValueViewSet


router = routers.DefaultRouter()
router.register('robots', RobotViewSet)
router.register('motions', MotionViewSet)
router.register('values', ValueViewSet)
