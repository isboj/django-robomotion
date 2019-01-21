from django.db import models
from django.conf import settings

import random, string


def random_key(n):
    """
    n文字のランダムな文字列を作成する(大文字・小文字英数字)
    :param n:
    :return:
    """
    key = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
    return ''.join(key)


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
    is_public = models.BooleanField(default=False)  # robotの共有可否
    share_key = models.CharField(max_length=10, default=random_key(10))  # 共有用key

    def save(self, *args, **kwargs):

        if self.id is None:
            # 新規作成のとき

            # TODO: share_keyが重複する可能性の考慮が必要
            self.share_key = random_key(10)  # なぜか、defaultでshare_keyが設定できないことがあるため

        super(Robot, self).save(*args, **kwargs)

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
    motion_num = models.IntegerField(blank=False)
    motion_category = models.CharField(max_length=100)
    value_info = models.TextField(blank=True)

    def save(self, *args, **kwargs):

        robot = self.robot  # ロボットを取得

        if self.id is None:
            # 新規作成の場合
            motions = robot.motions.all().order_by("motion_num")  # robotに関するモーションを取得
            motions_size = motions.count()
        else:
            # 更新の場合
            old_robot = Motion.objects.filter(id=self.id)[0].robot  # 更新前のロボットオブジェクト
            motions = robot.motions.exclude(id=self.id).order_by("motion_num")  # 更新するものは、除く
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

    def delete(self, *args, **kwargs):
        robot = self.robot  # 削除するmotionのrobotを取得
        self.recalc_motion_num(robot)  # motion_numの再計算を行う

        super(Motion, self).delete(*args, **kwargs)

    def recalc_motion_num(self, robot):
        """
        motion_numを再計算する
        :param robot: 再計算したいrobot
        :return:
        """
        motions = robot.motions.exclude(id=self.id).order_by("motion_num")  # self.idがなくなったことを想定
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
