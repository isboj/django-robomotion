from django.forms import ModelForm
from robocms.models import Robot, Motion


class RobotForm(ModelForm):
    """
    ロボットのフォーム
    """
    class Meta:
        model = Robot
        fields = ('user', 'robot_name')


class MotionFrom(ModelForm):
    """
    モーションのフォーム
    """
    class Meta:
        model = Motion
        fields = ('robot', 'motion_name', 'motion_category', 'value_info')
