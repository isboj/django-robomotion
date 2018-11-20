from django.shortcuts import render
import django_filters
from rest_framework import viewsets, filters
from rest_framework.decorators import detail_route, action
from rest_framework.response import Response
from django.core import exceptions

from robocms.models import Robot, Motion, Value
from .serializer import RobotSerializer, MotionSerializer, ValueSerializer


class RobotViewSet(viewsets.ModelViewSet):
    queryset = Robot.objects.all()
    serializer_class = RobotSerializer

    @action(methods=['GET'], detail=False)
    def get_robot_id(self, request):
        """
        ロボット名からIDを取得する

        ex: Pepperという名前のロボットのidを取得
        /robots/get_robot_id/?robot_name=Pepper

        :param request:
        :return:
        """
        response = {}
        if "robot_name" in request.query_params:
            robot_name = request.query_params["robot_name"]
        else:
            response["message"] = "query_params is invalid"
            response["status"] = False
            return Response(response)

        user = self.request.user  # ログイン中のユーザのロボットを取得
        try:
            robot = user.robots.all().get(robot_name=robot_name)
        except exceptions.ObjectDoesNotExist:
            response["message"] = "Robot name not exist."
            response["status"] = False
        else:  # tryで例外が発生しなったとき
            response["robot_name"] = robot_name
            response["robot_id"] = robot.id
            response["message"] = "Request is Good!"
            response["status"] = True

        return Response(response)

    @detail_route(methods=["GET"])
    def get_motion(self, request, pk=None):
        """
        ロボットのdetailルートから、モーションidを取得する

        ex: robot_id:8でpepper 01というモーションを取得する
        /robots/8/get_motion/?motion_name=pepper 01
        :param request:
        :param pk:
        :return:
        """
        response = {}
        if "motion_name" in request.query_params:
            motion_name = request.query_params["motion_name"]
        else:
            response["message"] = "query_params is invalid"
            response["status"] = False
            return Response(response)

        user = self.request.user
        # ロボットidはget_robot_idを行ったことにより、正確である前提
        robot = user.robots.all().get(id=pk)
        try:
            motion = robot.motions.all().get(motion_name=motion_name)
        except exceptions.ObjectDoesNotExist:
            response["message"] = "Motion name not exist."
            response["status"] = False
        else:
            response["motion_name"] = motion_name
            response["motion_id"] = motion.id
            response["status"] = True

        return Response(response)


class MotionViewSet(viewsets.ModelViewSet):
    queryset = Motion.objects.all()
    serializer_class = MotionSerializer

    @detail_route(methods=['GET'])
    def all_values(self, request, pk=None):
        """
        Motionに関するすべてのValueを取得する
        :param request:
        :param pk:
        :return:
        """
        motion = self.get_object()
        values = motion.values.all().order_by('id')  # id順にvalueを取得
        values = values.values_list('data', flat=True)  # 座標値(data)のみ取得
        return Response(list(values))

    @detail_route(methods=['GET'])
    def select_value(self, request, pk=None):
        """
        Motionに関する、countで指定したValueを取得する
        :param request:
        :param pk:
        :return:
        """
        query_dict = request.query_params
        count = request.query_params["count"]
        response = {}

        motion = self.get_object()
        values = motion.values.all().order_by('id')  # id順にvalueを取得
        response["size"] = len(values)
        response["count"] = int(count)
        response["data"] = values[int(count)].data  # 座標値(data)のみ取得
        return Response(response)


class ValueViewSet(viewsets.ModelViewSet):
    queryset = Value.objects.all()
    serializer_class = ValueSerializer
