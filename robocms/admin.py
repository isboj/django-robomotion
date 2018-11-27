from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Robot, Motion, Value

# robocmsをadmin上で編集できるようにする
admin.site.register(Robot)
admin.site.register(Motion)
admin.site.register(Value)

admin.site.register(get_user_model())
