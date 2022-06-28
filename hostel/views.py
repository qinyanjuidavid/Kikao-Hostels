from django.shortcuts import render, get_object_or_404
from accounts.models import Administrator
from accounts.permissions import IsAdminOrReadOnly, IsAdministrator, IsStudent
from hostel.models import Hostel, Rooms, Space
from hostel.serializers import HostelSerializer, RoomSerializer, SpaceSerializer
from rest_framework import generics, serializers, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class HostelAPIView(ModelViewSet):
    serializer_class = HostelSerializer
    permission_classes = [IsAuthenticated, IsAdministrator, IsAdminOrReadOnly]
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        hostelObj = Hostel.objects.all()
        return hostelObj

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset()
        serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        adminObj = Administrator.objects.get(user=request.user)
        serializer.save(added_by=adminObj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(queryset, data=request.data)
        serializer.is_valid(raise_exception=True)
        adminObj = Administrator.objects.get(user=request.user)
        serializer.save(added_by=adminObj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        queryset.delete()
        return Response(
            {"message": "Hostel was successfully deleted."},
            status=status.HTTP_204_NO_CONTENT
        )


class RoomAPIView(ModelViewSet):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated, IsAdministrator, IsAdminOrReadOnly]
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        roomObj = Rooms.objects.all()
        return roomObj

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset()
        serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        adminObj = Administrator.objects.get(user=request.user)
        serializer.save(added_by=adminObj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(queryset, data=request.data)
        serializer.is_valid(raise_exception=True)
        adminObj = Administrator.objects.get(user=request.user)
        serializer.save(added_by=adminObj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        queryset.delete()
        return Response(
            {"message": "Room was successfully deleted."},
            status=status.HTTP_204_NO_CONTENT
        )


class SpaceAPIVIew(ModelViewSet):
    serializer_class = SpaceSerializer
    permission_classes = [IsAuthenticated, IsAdministrator, IsAdminOrReadOnly]
    http_method_names = ["post", "get", "put", "delete"]

    def get_queryset(self):
        spaceObj = Space.objects.all()
        return spaceObj

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset()
        serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        adminObj = Administrator.objects.get(user=request.user)
        serializer.save(added_by=adminObj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(queryset, data=request.data)
        serializer.is_valid(raise_exception=True)
        adminObj = Administrator.objects.get(user=request.user)
        serializer.save(added_by=adminObj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        queryset.delete()
        return Response(
            {"message": "Space was successfully deleted."},
            status=status.HTTP_204_NO_CONTENT
        )


class HostelBookingAPI(ModelViewSet):
    serializer_class = HostelSerializer
    permission_classes = [IsAuthenticated, IsStudent]
    http_method_names = ["get", "post"]
