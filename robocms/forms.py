from django.forms import ModelForm
from robocms.models import Robot, Motion
from django import forms


class RobotForm(ModelForm):
    """
    ロボットのフォーム
    """
    class Meta:
        model = Robot
        fields = ('user', 'robot_name')
        exclude = ('user',)  # ユーザは入力できない

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')  # viewから値を受け取る
        super(RobotForm, self).__init__(*args, **kwargs)

    def clean(self):
        """
        複数フィールドのバリデーション
        :return:
        """
        cleaned_data = super(ModelForm, self).clean()
        robot_name = cleaned_data.get('robot_name')

        print(self.user, robot_name)
        if self.user.robots.filter(robot_name=robot_name).exists():
            # 既に、同名のロボットが存在していた時
            # TODO: updateの時自分自身を参照するため、条件を追加する必要あり
            raise forms.ValidationError('このロボット名は既に存在します')

        return cleaned_data


class MotionFrom(ModelForm):
    """
    モーションのフォーム
    """
    motion_name = forms.CharField(
        label="モーション名",
    )
    motion_category = forms.ChoiceField(
        choices=(
            ("unclassified", "未分類"),
        )
    )

    class Meta:
        model = Motion
        fields = ('robot', 'motion_name', 'motion_num', 'motion_category', 'value_info')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')  # viewから値を受け取る
        super(MotionFrom, self).__init__(*args, **kwargs)

        self.fields["robot"].queryset = self.user.robots.all()

        #self.fields["robot"] = forms.ChoiceField(
        #    choices=[(r, r.robot_name) for r in self.user.robots.all()]
        #)

    def clean(self):
        """
        複数フィールドのバリデーション
        :return:
        """
        cleaned_data = super(ModelForm, self).clean()
        robot = self.cleaned_data.get('robot')
        motion_name = cleaned_data.get('motion_name')

        if robot.motions.filter(motion_name=motion_name).exists():
            # 既に、同名のモーションが存在していた時
            # TODO: updateの時自分自身を参照するため、条件を追加する必要あり
            error_message = "{}のモーション: {} は既に存在します".format(robot.robot_name, motion_name)
            raise forms.ValidationError(error_message)

        return cleaned_data
