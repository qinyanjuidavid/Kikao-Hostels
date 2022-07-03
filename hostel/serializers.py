from hostel.models import Hostel, HostelBooking, Rooms, Space
from rest_framework import serializers


class HostelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hostel
        fields = ("id", "hostel_name", "gender",
                  "added_by", "created_at",
                  "updated_at")
        read_only_fields = ("id",)


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = ("id", "room_name", "hostel",
                  "room_type", "added_by", "created_at",
                  "updated_at",)
        read_only_fields = ("id",)


class SpaceSerializer(serializers.ModelSerializer):
    price = serializers.FloatField(required=True)

    class Meta:
        model = Space
        fields = ("id", "space_name", "room", "hostel",
                  "price", "vacant", "reserved", "added_by",
                  "created_at", "updated_at")
        read_only_fields = ("id",)


class HostelBookingSerializer(serializers.ModelSerializer):
    space = SpaceSerializer(read_only=True)

    class Meta:
        model = HostelBooking
        fields = ("space", "student", "admin",
                  "checkin_date", "checkout_date", "paid",
                  "accepted", "cleared")

        read_only_fields = ("id",)
