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

        # 番号を入れ替える必要があるとき
        if Motion.objects.filter(self.id).exists():
            print("SELF ID IS NOT NONE")
            motions.get(motion_num=self.motion_num).delete()

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
            motion_id_count = 0
            print('fdasfdsafdsafdsa')
            for i in range(motions_size):
                print("RANVGE I", i)
                if i is not self.motion_num:
                    print('MFSADF', i, motion_id_count)
                    Motion.objects.filter(id=motions[motion_id_count].id).update(motion_num=i)
                else:
                    motion_id_count += 1
                motion_id_count += 1
        super(Motion, self).save(*args, **kwargs)

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
