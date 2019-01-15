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
    """
    valueを取得するためのserializer
    登録は考慮していない
    """

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


class ValueSetSerializer(serializers.ModelSerializer):
    """
    valueフレームを登録するためのserializer
    """
    class Meta:
        model = Value
        fields = ('data',)

    def create(self, validated_data):
        motion = self.context["motion"]
        value = Value(
            motion=motion,
            value_num=0,
            data=validated_data['data']
        )
        value.save()
        return value

    def validate(self, attrs):
        """
        全体のバリデーション
        :param attrs:
        :return:
        """
        robot = self.context.get("robot")
        motion = self.context.get("motion")

        if robot is False:
            raise serializers.ValidationError("Robot does not exist.")
        elif motion is False:
            raise serializers.ValidationError("Motion does not exist.")

        return attrs
