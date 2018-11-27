from django.forms import ModelForm
from robocms.models import Robot, Motion, Value
from django import forms
from django.forms import Form
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class RobotForm(ModelForm):
    """
    ロボットのフォーム
    """
    class Meta:
        model = Robot
        fields = ('user', 'robot_name', 'is_public')
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

        same_name_robots = self.user.robots.filter(robot_name=robot_name)
        # updateアクションの際はエラーとならない。なお、同名のrobotが既に二つ以上あることは想定していない。
        if same_name_robots.count() > 0 and same_name_robots[0].id != self.instance.pk:
            # 既に、同名のロボットが存在していた時
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
        self.robot = None
        self.error_count = 0
        if "robot" in kwargs:
            # ロボットがurlから指定されていた場合
            self.robot = kwargs.pop('robot')
        super(MotionFrom, self).__init__(*args, **kwargs)

        self.fields["robot"].queryset = self.user.robots.all()
        if self.robot:
            # 指定されていたロボットのみ選択できる
            self.fields["robot"].initial = self.robot
            #self.fields["robot"].disabled = True
            # ロボットが定まるので、MotionNumも絞られる
            motion_num = self.robot.motions.count()
            self.fields["motion_num"] = forms.ChoiceField(
                choices=[(i, i) for i in range(motion_num+1)]
            )

    def clean_motion_name(self):
        """
        複数フィールドのバリデーション
        :return:
        """
        cleaned_data = super(ModelForm, self).clean()
        robot_ = self.cleaned_data.get('robot')
        motion_name = cleaned_data.get('motion_name')

        same_name_motions = robot_.motions.filter(motion_name=motion_name)
        # updateアクションの際はエラーとならない。なお、同名のmotionが既に二つ以上あることは想定していない。
        if same_name_motions.count() > 0 and same_name_motions[0].id != self.instance.pk:
            # 既に、同名のモーションが存在していた時
            error_message = "{}のモーション: {} は既に存在します".format(robot_.robot_name, motion_name)
            self.error_count += 1
            raise forms.ValidationError(error_message)

        return motion_name

    def clean(self):
        cleaned_data = super(ModelForm, self).clean()
        if self.error_count != 0:
            raise forms.ValidationError("エラーが{}つ存在します".format(self.error_count))
        return cleaned_data


class ValueMultipleDeleteForm(Form):

    checkboxes = forms.ModelMultipleChoiceField(
        Value.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
