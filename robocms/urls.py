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
    # robot_idに関するmotionの一覧表示
    path('robot/<int:robot_id>/motion/index', views.MotionIndexView.as_view(), name='motion_index'),
    path('motion/add', views.MotionCreateView.as_view(), name='motion_add'),  # 新規登録
    # 新規登録(ロボットは分かった状態)
    path("motion/<int:robot_id>/add", views.MotionCreateView.as_view(), name="motion_add_with_robot"),
    path('motion/<int:pk>/update', views.MotionUpdateView.as_view(), name='motion_update'),  # 編集
    path('motion/<int:pk>/delete', views.MotionDeleteView.as_view(), name='motion_delete'),  # 削除
    # Value関連
    path('motion/<int:motion_id>/value/index', views.value_index_in_motion, name='value_index'),
    path('motion/<int:motion_id>/value/index_delete', views.ValueMultipleDeleteView.as_view(), name='value_index_delete'),
    path('value/<int:pk>/detail', views.ValueDetailView.as_view(), name='value_detail'),  # 詳細
]
