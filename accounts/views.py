from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import UserCreationForm
#from django.contrib.auth.forms import UserCreationForm


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
