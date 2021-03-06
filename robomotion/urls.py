"""robomotion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from api_v0.urls import router as api_v0_router
from robocms.views import home

urlpatterns = [
    #path('', index),  # 最初のページ
    path('robocms/', include(('robocms.urls', 'robocms'), )),
    path('api_v0/', include(api_v0_router.urls)),
    # ログイン関連ビュー
    path('accounts/', include(('accounts.urls', 'accounts'), )),
    # auth api by jwt
    path('auth_api/', include('auth_api.urls')),
    path('admin/', admin.site.urls),

]
