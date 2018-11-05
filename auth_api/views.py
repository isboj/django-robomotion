from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class IndexViewSet(GenericAPIView):
    """
    ログインユーザの情報を取得する
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        data = {
            'username': request.user.username,
            'userid': request.user.id
            }
        return Response(data, status=status.HTTP_200_OK)
