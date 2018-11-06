from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.decorators import login_required


from .models import Robot, Motion
from .forms import RobotForm, MotionFrom

# === ロボットに関するView ===
def home(request):
    return render(request, 'robocms/home.html')


class RobotIndexView(generic.ListView):
    """
    ロボットの一覧表示
    """
    template_name = 'robocms/robot/index.html'
    context_object_name = 'robot_list'

    def get_queryset(self):
        user = self.request.user
        robots = user.robots.all()
        return robots


def robot_edit(request, pk=None):
    """
    ロボットの編集
    :param request:
    :param robot_id:
    :return:
    """

    if pk:
        # robot_idが指定されている(編集時)
        robot = get_object_or_404(Robot, pk=pk)
    else:
        # robot_idがない(新規作成時)
        robot = Robot()

    if request.method == "POST":
        # POSTされたとき
        form = RobotForm(request.POST, instance=robot)

        if form.is_valid():
            robot = form.save(commit=False)
            robot.user = request.user
            robot.save()
            return redirect('robocms:robot_index')

    else:
        # Getの時
        form = RobotForm(instance=robot)

    return render(request, 'robocms/edit.html', dict(form=form, robot_id=pk))

# ===モーションに関するView===

def motion_index_in_robot(request, robot_id):
    """
    ロボットに属するモーションの一覧表示
    :param request:
    :param robot_id:
    :return:
    """
    robot = Robot.objects.get(id=robot_id)
    motion_list = robot.motions.all()
    context = {
        'robot': robot,
        'motion_list': motion_list
    }
    return render(request, 'robocms/motion/index.html', context)


def motion_edit(request, pk=None):
    if pk:
        # motion_idが指定されている
        motion = get_object_or_404(Motion, pk=pk)
    else:
        # motion_idがないとき
        motion = Motion()

    if request.method == "POST":
        form = MotionFrom(request.POST, instance=motion)

        if form.is_valid():
            motion = form.save(commit=False)
            motion.save()
            return redirect('robocms:robot_index')

    else:
        # Getの時
        form = MotionFrom(instance=motion)

    return render(request, 'robocms/edit.html', dict(form=form, motion_id=pk))

# ===valueに関するView===
