from django.contrib import admin
from django.contrib.auth.models import Group

from accounts.models import (Administrator, Student, User,
                             Course)
admin.site.unregister(Group)


@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role",
                    "phone", "is_active", "is_admin",
                    "is_staff", "timestamp")
    list_filter = ("is_active", "is_admin", "is_staff", "role")


admin.site.register(Student)
admin.site.register(Administrator)
admin.site.register(Course)
