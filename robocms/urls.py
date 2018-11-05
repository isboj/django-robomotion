from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('index/', login_required(views.IndexView.as_view()), name='index'),  # 一覧
    path('add/', views.robot_edit, name='add'),  # 新規登録
    path('<int:pk>/edit/', views.robot_edit, name='edit'),  # 編集

]
