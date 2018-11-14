from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import UserCreationForm
#from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib import messages

from django.contrib.auth.forms import PasswordChangeForm

from django.views.generic import FormView


def signup(request):
    """
    新規登録するビュー
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # ログインしてあげる
            return redirect('top')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/signup.html', {'form': form})


class PasswordChangeView(FormView):
    template_name = 'accounts/password_change.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('robocms:home')

    def get_form_kwargs(self):
        kwargs = super(PasswordChangeView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request,
                         "パスワードの変更が完了しました。再度ログインしてください。",
                         extra_tags="check")
        return super(PasswordChangeView, self).form_valid(form)
