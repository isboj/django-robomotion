from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.decorators import login_required


from .models import Robot
from .forms import RobotForm


def home(request):
    return render(request, 'robocms/home.html')


class IndexView(generic.ListView):
    """
    ロボットの一覧表示
    """
    template_name = 'robocms/index.html'
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
            return redirect('robocms:home')

    else:
        # Getの時
        form = RobotForm(instance=robot)

    return render(request, 'robocms/edit.html', dict(form=form, robot_id=pk))
