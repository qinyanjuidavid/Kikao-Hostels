from django.db import models

from accounts.models import Administrator, Student, TrackingModel
from django.utils.translation import gettext as _


class Hostel(TrackingModel):
    gender_choices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    hostel_name = models.CharField(
        _("hostel name"), max_length=57,
        unique=True)
    gender = models.CharField(
        _('gender'), choices=gender_choices,
        max_length=20, default="Male"
    )
    added_by = models.ForeignKey(Administrator, blank=True,
                                 on_delete=models.DO_NOTHING,
                                 null=True)

    def __str__(self):
        return self.hostel_name

    class Meta:
        verbose_name_plural = "Hostels"
        ordering = ["-id"]


class Rooms(TrackingModel):
    room_choices = (
        ("Single Occupancy", "Single Occupancy"),
        ("Shared Occupancy", "Shared Occupancy"),
        ("Reserved Occupancy", "Reserved Occupancy")
    )
    room_name = models.CharField(
        _("room name"), max_length=26
    )
    room_type = models.CharField(
        _("room type"), max_length=26,
        choices=room_choices,
        default="Shared Occupancy"
    )
    hostel = models.ForeignKey(
        Hostel,
        on_delete=models.CASCADE)
    added_by = models.ForeignKey(Administrator, blank=True,
                                 on_delete=models.DO_NOTHING,
                                 null=True)

    def __str__(self):
        return self.room_name

    class Meta:
        verbose_name_plural = "Rooms"
        ordering = ["-id"]


class Space(TrackingModel):
    space_name = models.CharField(
        _("space name"), max_length=26,
        help_text="eg. space 1, space 2,..."
    )
    room = models.ForeignKey(Rooms,
                             on_delete=models.CASCADE)
    hostel = models.ForeignKey(Hostel, on_delete=models.PROTECT,
                               blank=True, null=True)
    price = models.FloatField(_("price"), default=0.00)
    vacant = models.BooleanField(_("vacant"), default=True)
    reserved = models.BooleanField(_("reserved"), default=False)
    added_by = models.ForeignKey(Administrator, blank=True,
                                 on_delete=models.DO_NOTHING,
                                 null=True)

    def __str__(self):
        return self.space_name

    class Meta:
        verbose_name_plural = "Spaces"
        ordering = ["-id"]


class HostelBooking(TrackingModel):
    space = models.ForeignKey(Space, on_delete=models.PROTECT)
    student = models.OneToOneField(Student, blank=True, null=True,
                                   on_delete=models.DO_NOTHING)
    admin = models.ForeignKey(Administrator,
                              on_delete=models.DO_NOTHING,
                              blank=True, null=True)
    checkin_date = models.DateTimeField(
        _("checkin date"), null=True)
    checkout_date = models.DateTimeField(
        _("checkout date"), null=True)
    paid = models.BooleanField(_("paid"),
                               default=False)
    accepted = models.BooleanField(_("accepted"),
                                   default=False)
    cleared = models.BooleanField(
        _("cleared"), default=False,
        help_text="student should be cleared before checking out"
    )

    def __str__(self):
        return self.student.user.username

    class Meta:
        verbose_name_plural = "Hostel Booking"
        ordering = ["-id"]
