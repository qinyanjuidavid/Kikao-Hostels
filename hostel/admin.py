from django.contrib import admin
from hostel.models import (Hostel, Rooms,
                           Space, HostelBooking)
admin.site.register(Hostel)
admin.site.register(Rooms)
admin.site.register(Space)
admin.site.register(HostelBooking)
