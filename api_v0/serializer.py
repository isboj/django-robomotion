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


class ValueListSerializer(serializers.ModelSerializer):

    motion_name = serializers.SerializerMethodField()
    motion_num = serializers.SerializerMethodField()
    robot_name = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    class Meta:
        model = Value
        fields = ('id', 'data', 'motion_name', 'motion_num', 'robot_name', 'size', 'count')

    def get_motion_name(self, instance):
        return instance.motion.motion_name

    def get_motion_num(self, instance):
        return instance.motion.motion_num

    def get_robot_name(self, instance):
        return instance.motion.robot.robot_name

    def get_size(self, instance):
        return self.context["size"]

    def get_count(self, instance):
        if "count" in self.context:
            return int(self.context["count"])
        return "Count return only use count param!"
