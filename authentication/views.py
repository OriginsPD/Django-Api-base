'''
    Templates View for Index Page along with signup and login pages
    Template, CreateView and AuthorizeView
'''
# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from djoser.views import UserViewSet
from rest_framework import status
from .serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class ActivateUser(UserViewSet):
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())

        # this line is the only change from the base implementation.
        kwargs['data'] = {"uid": self.kwargs['uid'],
                          "token": self.kwargs['token']}

        return serializer_class(*args, **kwargs)

    def activation(self, request, uid, token, *args, **kwargs):
        if super().activation(request, *args, **kwargs):
            return Response({"message": "Account activation successfully"},
                            status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "Account activation failed"},
                            status=status.HTTP_404_NOT_FOUND)
