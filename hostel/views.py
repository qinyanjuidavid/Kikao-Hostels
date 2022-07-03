from django.shortcuts import render, get_object_or_404
from accounts.models import Administrator, Course, Student
from accounts.permissions import IsAdminOrReadOnly, IsAdministrator, IsStudent
from accounts.serializers import CourseSerializer
from hostel.models import Hostel, HostelBooking, Rooms, Space
from hostel.serializers import HostelBookingSerializer, HostelSerializer, RoomSerializer, SpaceSerializer
from rest_framework import generics, serializers, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from rest_framework.decorators import action


class CourseAPIView(ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsAdministrator, IsAdminOrReadOnly]
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        courseQs = Course.objects.all()
        return courseQs

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
        if request.user.role == "Administrator":
            adminObj = Administrator.objects.get(user=request.user)
            serializer.save(added_by=adminObj)
        else:
            return Response(
                {"message": "You are not authorized to perform this action."},
                status=status.HTTP_200_OK
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid()
        if request.user.role == "Administrator":
            adminObj = Administrator.objects.get(user=request.user)
            serializer.save(added_by=adminObj)
        else:
            return Response(
                {"message": "You are not authorized to perform this action."},
                status=status.HTTP_200_OK
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        if request.user.role == "Administrator":
            queryset.delete()
        else:
            return Response(
                {"message": "You are not authorized to perform this action."},
                status=status.HTTP_200_OK
            )
        return Response(
            {"message": "Course was successfully deleted."},
            status=status.HTTP_204_NO_CONTENT
        )


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
        if request.user.role == "Administrator":
            adminObj = Administrator.objects.get(user=request.user)
            serializer.save(added_by=adminObj)
        else:
            return Response(
                {"message": "You are not authorized to perform this action."},
                status=status.HTTP_200_OK
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(queryset, data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.user.role == "Administrator":
            adminObj = Administrator.objects.get(user=request.user)
            serializer.save(added_by=adminObj)
        else:
            return Response(
                {"message": "You are not authorized to perform this action."},
                status=status.HTTP_200_OK
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        if request.user.role == "Administrator":
            queryset.delete()
        else:
            return Response(
                {"message": "You are not authorized to perform this action."},
                status=status.HTTP_200_OK
            )
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
        if request.user.role == "Administrator":
            roomQuery = Rooms.objects.filter(
                Q(room_name=serializer.validated_data["room_name"]) &
                Q(hostel=serializer.validated_data["hostel"])
            )
            if roomQuery.exists():
                return Response(
                    {"message": "Room already exists"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                adminObj = Administrator.objects.get(user=request.user)
                serializer.save(added_by=adminObj)
        else:
            return Response(
                {"message": "You are not authorized to perform this action."},
                status=status.HTTP_200_OK
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(queryset, data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.user.role == "Administrator":
            adminObj = Administrator.objects.get(user=request.user)
            serializer.save(added_by=adminObj)
        else:
            return Response(
                {"message": "You are not authorized to perform this action."},
                status=status.HTTP_200_OK
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        if request.user.role == "Administrator":
            queryset.delete()
        else:
            return Response(
                {"message": "You are not authorized to perform this action."},
                status=status.HTTP_200_OK
            )
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
        if request.user.role == "Administrator":
            spaceQs = Space.objects.filter(
                Q(space_name=serializer.validated_data["space_name"]) &
                Q(room=serializer.validated_data["room"]) &
                Q(hostel=serializer.validated_data["room"].hostel)
            )
            if spaceQs.exists():
                return Response(
                    {"message": "Space already exists"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                adminObj = Administrator.objects.get(user=request.user)
                hostel = serializer.validated_data["room"].hostel
                serializer.save(added_by=adminObj, hostel=hostel)
        else:
            return Response(
                {"message": "You are not authorized to perform this action."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(queryset, data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.user.role == "Administrator":
            adminObj = Administrator.objects.get(user=request.user)
            hostel = serializer.validated_data["room"].hostel
            serializer.save(added_by=adminObj, hostel=hostel)
        else:
            return Response(
                {"message": "You are not authorized to perform this action."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        if request.user.role == "Administrator":
            queryset.delete()
        else:
            return Response(
                {"message": "You are not authorized to perform this action."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {"message": "Space was successfully deleted."},
            status=status.HTTP_204_NO_CONTENT
        )


class HostelBookingAPI(ModelViewSet):
    serializer_class = SpaceSerializer
    permission_classes = [IsAuthenticated, IsStudent]
    http_method_names = ["get", "post"]

    def get_queryset(self):
        spaceQs = Space.objects.filter(
            Q(vacant=True),
            Q(reserved=False)
        )
        return spaceQs

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset()
        serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_name="book-hostel")
    def book(self, request, pk=None, *args, **kwargs):
        serializer = HostelBookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        studentQuery = Student.objects.get(user=request.user)
        bookedHostelQuery = HostelBooking.objects.filter(
            Q(student=studentQuery) &
            Q(cleared=False)
        )
        if bookedHostelQuery.exists():
            return Response(
                {"message": "You have already booked another hostel."},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            hostelObj = HostelBooking.objects.create(
                space=Space.objects.get(
                    Q(id=pk)
                ),
                student=studentQuery,
                space__vacant=True
            )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"],)
    def myhostel(self, request, *args, **kwargs):
        hostelQs = HostelBooking.objects.filter(
            Q(student=Student.objects.get(
                user=request.user
            )),
            Q(space__vacant=False)
        )
        serializer = HostelBookingSerializer(hostelQs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookedHostels(ModelViewSet):
    serializer_class = HostelBookingSerializer
    permission_classes = [IsAuthenticated, IsAdministrator]
    http_method_names = ["put", "post", "get"]

    def get_queryset(self):
        bookedHostel = HostelBooking.objects.all()
        return bookedHostel

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
        adminObj = Administrator.objects.get(
            Q(user=request.user)
        )
        serializer.save(admin=adminObj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(queryset, data=request.data)
        serializer.is_valid(raise_exception=True)
        adminObj = Administrator.objects.get(user=request.user)
        serializer.save(admin=adminObj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
