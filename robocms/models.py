from django.db import models


class Robot(models.Model):
    """
    ロボット情報
    """
    robot_name = models.CharField(max_length=100)
    robot_category = models.CharField(max_length=100)

    def __repr__(self):
        # 主キーとnameを返して見やすくする
        # ex:  1: pepper
        return "{}: {}".format(self.pk, self.robot_name)

    __str__ = __repr__  # __str__も同じ


class Motion(models.Model):
    """
    モーション情報
    """
    robot = models.ForeignKey(Robot, on_delete=models.CASCADE)
    motion_name = models.CharField(max_length=100)
    motion_category = models.CharField(max_length=100)
    value_info = models.TextField(blank=True)

    def __repr__(self):
        # 主キーとnameを返して見やすくする
        # ex:  1: motion_01
        return "{}: {}".format(self.pk, self.motion_name)

    __str__ = __repr__  # __str__も同じ


class Value(models.Model):
    """
   モーションデータ
   主に座標値など
    """
    motion = models.ForeignKey(Motion, related_name="values", on_delete=models.CASCADE)
    data = models.TextField(blank=True)
