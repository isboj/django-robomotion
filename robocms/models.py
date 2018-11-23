from django.db import models
from django.conf import settings


class Robot(models.Model):
    """
    ロボット情報
    """
    # robot auth association model
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='robots',
                             on_delete=models.CASCADE)
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
    robot = models.ForeignKey(Robot, related_name='motions', on_delete=models.CASCADE)
    motion_name = models.CharField(max_length=100)
    motion_num = models.IntegerField(blank=True)
    motion_category = models.CharField(max_length=100)
    value_info = models.TextField(blank=True)

    def save(self, *args, **kwargs):

        robot = self.robot
        motions = robot.motions.all().order_by("motion_num")
        motions_size = motions.count()

        # 番号を入れ替える必要があるとき(更新の場合)
        if self.id is not None:
            old_robot = Motion.objects.filter(id=self.id)[0].robot  # 更新前のロボットオブジェクト
            motions.filter(id=self.id).delete()  # 更新の場合は更新するものを、まず削除
            motions_size = motions.count()

            # 更新後に異なるrobotに所属する場合
            if old_robot.id != robot.id:
                # 所属するrobotが違う場合は、古いロボットのモーションを再計算する
                self.recalc_motion_num(old_robot)

        if len(motions) < 1:
            # モーションが存在しないとき(最初のモーション作成)
            self.motion_num = 0  # 最初は0にする
        elif self.motion_num < 0 or len(motions) < self.motion_num:
            # motion_numがマイナス、もしくは大きいとき(既にあるmotion_numと被らない)
            for i, motion in enumerate(motions):
                Motion.objects.filter(id=motion.id).update(motion_num=i)
            self.motion_num = motions_size  # 最後の値に設定
        else:
            # 入れ替える必要のあるオブジェクト
            is_passed_num = 0  # 新規の挿入が出来たかどうが(intでないといけない)
            for i in range(motions_size+1):
                if i is not self.motion_num:
                    # 挿入したい番号でない場合
                    # すべてのmotionに対して番号の更新を行う。(updateアクションを考慮している)
                    Motion.objects.filter(id=motions[i - is_passed_num].id).update(motion_num=i)
                else:
                    # 番号を挿入したら、一つずらす
                    is_passed_num = 1

        super(Motion, self).save(*args, **kwargs)

    def recalc_motion_num(self, robot):
        """
        motion_numを再計算する
        :param robot: 再計算したいrobot
        :return:
        """
        motions = robot.motions.all().order_by("motion_num")
        motions.filter(id=self.id).delete()  # self.idがなくなった場合の再計算を行う
        # TODO: 削除の場合はすべてfor分を回す必要はないと思う（途中から開始で良いと思う）
        for i, obj in enumerate(motions):
            Motion.objects.filter(id=obj.id).update(motion_num=i)

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
    value_num = models.IntegerField(null=True, blank=True)
    data = models.TextField(blank=True)
