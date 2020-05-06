from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404, render
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST,
                                   HTTP_404_NOT_FOUND)

from .models import Image, Mall
from .serializers import ImageSerializer, MallSerializer, UserSerializer

User = get_user_model()


class LoginView(viewsets.ViewSet):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'},
                            status=HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.pk,
                         'username': user.username, 'email': user.email,
                         'created': token.created,
                         'first_name': user.first_name,
                         }, status=HTTP_200_OK)


class UserView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = User.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 100
        page = paginator.paginate_queryset(queryset, request)
        serializer = UserSerializer(page, many=True).data

        return Response(paginator.get_paginated_response(serializer).data)

    def retrieve(self, request, pk=None):
        item = get_object_or_404(pk=pk)
        serializer = UserSerializer(item)
        return Response(serializer.data)

    def create(self, request):
        data = request.data.copy()
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def update(self, request, pk=None):
        queryset = User.objects.all()
        instance = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = User.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        item.delete()
        return Response({"message": "user deleted"}, status=status.HTTP_200_OK)



class ImageView(viewsets.ViewSet):
    # permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = Image.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 100
        page = paginator.paginate_queryset(queryset, request)
        serializer = ImageSerializer(page, many=True).data
        return Response({"results": serializer})

    def create(self, request):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = Image.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        item.delete()
        return Response({"message": "item deleted"}, status=status.HTTP_200_OK)


class MallView(viewsets.ViewSet):
    # permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = Mall.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 100
        page = paginator.paginate_queryset(queryset, request)
        serializer = MallSerializer(page, many=True).data
        return Response({"results": serializer})

    def create(self, request):
        data = request.data.copy()
        data["attachedImages"] = [int(image) for image in data["attachedImages"].split(",")]
        serializer = MallSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        queryset = Mall.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = MallSerializer(instance=item, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = Mall.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        item.delete()
        return Response({"message": "item deleted"}, status=status.HTTP_200_OK)
