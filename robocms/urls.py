from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # ロボット関連
    path('robot/', login_required(views.RobotIndexView.as_view()), name='robot_index'),  # 一覧
    path('robot/add/', views.robot_edit, name='robot_add'),  # 新規登録
    path('robot/<int:pk>/edit/', views.robot_edit, name='robot_edit'),  # 編集
    # モーション関連
    path('motion/<int:robot_id>/index', views.motion_index_in_robot, name='motion_index'),
    path('motion/add', views.motion_edit, name='motion_add'),
]
