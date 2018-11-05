from django.forms import ModelForm
from robocms.models import Robot

class RobotForm(ModelForm):
    """
    ロボットのフォーム
    """
    class Meta:
        model = Robot
        fields = ('user', 'robot_name')
