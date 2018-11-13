from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

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


class RobotCreateView(CreateView):
    """
    ロボット新規作成
    """
    model = Robot
    template_name = 'robocms/edit.html'
    form_class = RobotForm
    success_url = "/robocms/"

    # ログインしているユーザを設定
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(RobotCreateView, self).form_valid(form)

    # kwargsで値渡し
    def get_form_kwargs(self):
        kwargs = super(RobotCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class RobotDeleteView(DeleteView):
    """
    ロボット削除
    """
    model = Robot
    success_url = reverse_lazy("robocms:robot_index")

    def get(self, request, *args, **kwargs):
        # 確認ビューは表示しない
        # 確認は、ポップアップにて行う
        return self.post(request, *args, **kwargs)


class RobotUpdateView(UpdateView):
    """
    ロボット更新
    """
    model = Robot
    template_name = 'robocms/edit.html'
    form_class = RobotForm
    success_url = "/robocms/"

    # kwargsで値渡し
    def get_form_kwargs(self):
        kwargs = super(RobotUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


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


class MotionCreateView(CreateView):
    """
    モーション新規作成
    """
    model = Motion
    template_name = 'robocms/edit.html'
    form_class = MotionFrom
    success_url = "/robocms/"

    # kwargsで値渡し
    def get_form_kwargs(self):
        kwargs = super(MotionCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

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


def value_index_in_motion(request, motion_id):
    """
    モーションに属するValueの表示
    :param request:
    :param motion_id:
    :return:
    """
    motion = Motion.objects.get(id=motion_id)
    value_list = motion.values.all()
    context = {
        'motion': motion,
        'value_list': value_list
    }
    return render(request, 'robocms/value/index.html', context)

