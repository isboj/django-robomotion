from django.contrib import admin

from .models import Robot, Motion, Value

# robocmsをadmin上で編集できるようにする
admin.site.register(Robot)
admin.site.register(Motion)
admin.site.register(Value)
