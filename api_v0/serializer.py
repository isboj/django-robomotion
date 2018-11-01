from rest_framework import serializers

from robocms.models import Robot, Motion, Value


class RobotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Robot
        fields = ('robot_name', 'robot_category')


class MotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motion
        fields = ('robot', 'motion_name', 'motion_category', 'value_info')


class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Value
        fields = ('motion', 'data')
