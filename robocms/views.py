from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib import messages

from .models import Robot, Motion, Value
from .forms import RobotForm, MotionFrom, ValueMultipleDeleteForm

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
    success_url = reverse_lazy('robocms:robot_index')

    # ログインしているユーザを設定
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request,
                         "{}を追加しました".format(form.instance.robot_name),
                         extra_tags="check")
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

    def delete(self, request, *args, **kwargs):
        object_ = self.get_object()
        messages.success(self.request,
                         "{}の削除が完了しました".format(object_.robot_name),
                         extra_tags="check")
        return super(RobotDeleteView, self).delete(request, *args, **kwargs)


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

class MotionIndexView(generic.ListView):
    """
    ロボットに関するモーションの一覧表示
    """
    template_name = 'robocms/motion/index.html'
    context_object_name = 'motion_list'

    def get_queryset(self):
        # TODO: ログインユーザの確認が必要
        robot = Robot.objects.get(id=self.kwargs["robot_id"])
        motion_list = robot.motions.all().order_by("motion_num")
        return motion_list

    def get_context_data(self, **kwargs):
        context = super(MotionIndexView, self).get_context_data(**kwargs)
        # urlからvalueを取得
        robot = Robot.objects.get(id=self.kwargs["robot_id"])
        context['robot'] = robot  # Customize this queryset to your liking
        return context


class MotionCreateView(CreateView):
    """
    モーション新規作成
    """
    model = Motion
    template_name = 'robocms/edit.html'
    form_class = MotionFrom
    #success_url = "/robocms/"

    # kwargsで値渡し
    def get_form_kwargs(self):
        kwargs = super(MotionCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        if "robot_id" in self.kwargs:
            # Motionを作成するロボットがわかっているとき
            kwargs['robot'] = Robot.objects.get(id=self.kwargs["robot_id"])
        return kwargs

    def get_success_url(self):
        robot_id = self.object.robot.id
        return reverse_lazy('robocms:motion_index', kwargs={'robot_id': robot_id})


class MotionUpdateView(UpdateView):
    """
    モーション更新
    """
    model = Motion
    template_name = 'robocms/edit.html'
    form_class = MotionFrom
    #success_url = "/robocms/"

    # kwargsで値渡し
    def get_form_kwargs(self):
        kwargs = super(MotionUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        #kwargs["pk"] = self.kwargs["pk"]
        return kwargs

    def get_success_url(self):
        robot_id = self.object.robot.id
        return reverse_lazy('robocms:motion_index', kwargs={'robot_id': robot_id})


class MotionDeleteView(DeleteView):
    """
    モーション削除
    """
    model = Motion
    #success_url = reverse_lazy("robocms:robot_index")

    def get(self, request, *args, **kwargs):
        # 確認ビューは表示しない
        # 確認は、ポップアップにて行う
        return self.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        object_ = self.get_object()
        messages.success(self.request,
                         "{}の削除が完了しました".format(object_.motion_name),
                         extra_tags="check")
        return super(MotionDeleteView, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        robot_id = self.object.robot.id
        return reverse_lazy('robocms:motion_index', kwargs={'robot_id': robot_id})



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


class ValueMultipleDeleteView(FormView):
    """
    バリュー(フレーム)の一覧表示、および選択削除機能
    """

    form_class = ValueMultipleDeleteForm
    template_name = 'robocms/value/multiple_delete.html'

    def get_context_data(self, **kwargs):
        context = super(ValueMultipleDeleteView, self).get_context_data(**kwargs)
        # urlからvalueを取得
        motion = Motion.objects.get(id=self.kwargs["motion_id"])
        context['objects'] = motion.values.all()  # Customize this queryset to your liking
        return context

    def get_form(self, form_class=None):
        form = super(ValueMultipleDeleteView, self).get_form(form_class)
        #form.fields['checkboxes'].queryset = Value.objects.all()
        # urlからvalueを取得
        motion = Motion.objects.get(id=self.kwargs["motion_id"])
        form.fields['checkboxes'].queryset = motion.values.all()
        return form

    def form_valid(self, form):
        qs = Value.objects.filter(
            pk__in=list(map(int, self.request.POST.getlist('checkboxes')))
        )
        qs_len = len(qs)
        qs.delete()
        motion = Motion.objects.get(id=self.kwargs["motion_id"])
        messages.success(self.request,
                         "{}個のフレーム削除が完了しました".format(qs_len),
                         extra_tags="check")
        # 同じビューにリダイレクト
        return HttpResponseRedirect(reverse_lazy('robocms:value_index_delete', kwargs={'motion_id': motion.id}))
