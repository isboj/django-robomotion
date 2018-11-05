from django.urls import path

from rest_framework_jwt.views import obtain_jwt_token
from . import views

urlpatterns = [
    path('login', obtain_jwt_token, name='login'),
    path('index', views.IndexViewSet.as_view(), name='index')
]
