from django.shortcuts import render
import django_filters
from rest_framework import viewsets, filters
from rest_framework.decorators import detail_route, action
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.views import APIView
from django.core import exceptions
from django.contrib.auth import get_user_model

from robocms.models import Robot, Motion, Value
from .serializer import RobotSerializer, MotionSerializer, ValueSerializer
from .serializer import ValueListSerializer, ValueSetSerializer


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


class RobotValueListAPIView(ListAPIView):
    """
    ロボットが所持するvalue(フレーム)の一覧を返す

    問い合わせ例
    -------------
    ex: robot_id=1のvalue(フレーム)一覧を取得::

        /robot_values/1

    ex: robot_id=1のvalue(フレーム)の0番目を取得::

        /robot_values/1?count=0

    ex: robot_id=1のmotionのうち、motion_id=2の一覧を取得::

        /robot_values/1?motion_id=2

    ex: robot_id=1でmotion_id=2のvalue(フレーム)の0番目を取得::

        /robot_values/1?motion_id=2&count=0
    """

    queryset = Value.objects.all()
    serializer_class = ValueListSerializer
    http_method_names = ['get', ]  # Getしか受け付けない

    authentication_classes = ()
    permission_classes = ()

    def __init__(self, *args, **kwargs):
        super(RobotValueListAPIView, self).__init__(*args, **kwargs)
        self.values = None
        self.size = 0

    def get_queryset(self):
        robot_id = self.kwargs["robot_id"]
        # 指定されたrobotを取得
        self.values = Value.objects.filter(motion__robot_id=robot_id).order_by("motion__motion_num", "id")
        self.size = self.values.count()  # 取得したvaluesのサイズ
        if "motion_id" in self.request.query_params:
            # motionが指定されている場合
            motion_id = self.request.query_params["motion_id"]
            # valuesの絞り込みにmotionも含める
            self.values = Value.objects.filter(motion__robot_id=robot_id, motion_id=motion_id).order_by("id")
            self.size = self.values.count()  # valuesのサイズを更新

        if "count" in self.request.query_params:
            # countが指定されている場合
            # *ここでは、サイズの更新は行わない。
            count = self.request.query_params["count"]
            self.values = self.values[int(count):int(count)+1]  # countの部分だけ返す
        return self.values

    def get_serializer_context(self):
        # serializerに渡す値
        context = {}
        if "count" in self.request.query_params:
            context["count"] = self.request.query_params["count"]
        context["size"] = self.size
        return context


class ShareRobotValueListAPIView(ListAPIView):
    """
    共有が許可されているRobotのvalue(フレーム)を取得する

    問い合わせ例
    -------------
    ex: share_key=0123456789のvalue(フレーム)一覧を取得::

        /share_key/0123456789

    ex: share_key=0123456789のvalue(フレーム)の0番目を取得::

        /share_key/0123456789?count=0

    share_keyもしくは共有が許可されていない場合のレスポンスは、
    空列( [] )となります。
    """

    queryset = Value.objects.all()
    serializer_class = ValueListSerializer
    http_method_names = ['get', ]  # Getしか受け付けない

    authentication_classes = ()
    permission_classes = ()

    def __init__(self, *args, **kwargs):
        super(ShareRobotValueListAPIView, self).__init__(*args, **kwargs)
        self.values = None
        self.size = 0

    def get_queryset(self):
        share_key = self.kwargs["share_key"]

        robots = Robot.objects.filter(share_key=share_key)
        # TODO: エラーメッセージ[Exception]を返してあげたほうが、親切
        if robots.count() > 0:
            # share_keyに合致するrobotが存在する場合
            if not robots[0].is_public:
                # is_public = Trueでないときは、返さない
                return None
        else:
            # share_keyに合致するrobotが存在しない
            return None
        # share_keyに基づいて取得
        self.values = Value.objects.filter(motion__robot__share_key=share_key).order_by("motion__motion_num", "id")
        self.size = self.values.count()  # 取得したvaluesのサイズ

        if "count" in self.request.query_params:
            # countが指定されている場合
            # *ここでは、サイズの更新は行わない。
            count = self.request.query_params["count"]
            self.values = self.values[int(count):int(count) + 1]  # countの部分だけ返す
        return self.values

    def get_serializer_context(self):
        # serializerに渡す値
        context = {}
        if "count" in self.request.query_params:
            context["count"] = self.request.query_params["count"]
        context["size"] = self.size
        return context


class ValueSetView(ListCreateAPIView):
    """
    value登録用

    ログインが必要(ユーザに基づき、robotとmotionを検索するため)

    問い合わせ例: (POST)
    まず、JWTによるログインを行い、リクエストヘッダに認証情報を含める必要がある

    ex: robot_name=pepper, motion_name=motion01にvalueを登録したいとき::

        /value_set/pepper/motion01

    """
    serializer_class = ValueSetSerializer
    queryset = Value.objects.all()

    #authentication_classes = ()
    #permission_classes = ()

    def get_serializer_context(self):
        # serializerに渡す値
        context = {}
        robot_name = self.kwargs["robot_name"]
        motion_name = self.kwargs["motion_name"]

        user = self.request.user
        #user = get_user_model()
        #user = user.objects.get(username="test")

        if user.robots.filter(robot_name=robot_name).exists():
            # robotが存在したとき
            context["robot"] = user.robots.get(robot_name=self.kwargs["robot_name"])

            if context["robot"].motions.filter(motion_name=motion_name).exists():
                # motionが存在したとき
                context["motion"] = context["robot"].motions.get(motion_name=motion_name)
            else:
                # motionが存在しないとき
                context["motion"] = False
        else:
            # robotが存在しないとき
            context["robot"] = False

        return context







