from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # ロボット関連
    path('robot/', login_required(views.RobotIndexView.as_view()), name='robot_index'),  # 一覧
    path('robot/add/', views.RobotCreateView.as_view(), name='robot_add'),  # 新規登録
    path('robot/<int:pk>/update/', views.RobotUpdateView.as_view(), name='robot_update'),  # 編集
    path('robot/<int:pk>/delete/', views.RobotDeleteView.as_view(), name='robot_delete'),  # 削除
    # モーション関連
    path('motion/<int:robot_id>/index', views.motion_index_in_robot, name='motion_index'),
    path('motion/add', views.MotionCreateView.as_view(), name='motion_add'),
    # Value関連
    path('value/<int:motion_id>/index', views.value_index_in_motion, name='value_index')

]
