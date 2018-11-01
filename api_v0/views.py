from django.shortcuts import render
import django_filters
from rest_framework import viewsets, filters
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from robocms.models import Robot, Motion, Value
from .serializer import RobotSerializer, MotionSerializer, ValueSerializer


class RobotViewSet(viewsets.ModelViewSet):
    queryset = Robot.objects.all()
    serializer_class = RobotSerializer


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
