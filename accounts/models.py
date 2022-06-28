from enum import unique
from django.contrib.auth import validators
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import (
    MaxLengthValidator,
    MaxValueValidator,
    MinLengthValidator)


class TrackingModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class CustomerManager(BaseUserManager):
    def create_user(self, email, username, password=None, is_active=True, is_admin=False, is_staff=False, role=""):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        if not username:
            raise ValueError("Users must have a username")
        user_obj = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user_obj.set_password(password)
        user_obj.is_active = is_active
        user_obj.is_admin = is_admin
        user_obj.is_staff = is_staff
        user_obj.role = role
        user_obj.save(using=self._db)

        return user_obj

    def create_staff(self, email, username, password=None):
        user = self.create_user(
            email, username, password=password, is_active=True,
            is_staff=True, is_admin=False, role="Administrator",
        )
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email, username, password=password, is_active=True,
            is_staff=True, is_admin=True, role="Administrator"
        )
        return user


class User(AbstractBaseUser, TrackingModel):
    username_validator = UnicodeUsernameValidator()

    Role_choices = (
        ('Administrator', 'Administrator'),
        ('Student', 'Student')
    )
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    full_name = models.CharField(_('full name'),
                                 max_length=150, blank=True, null=True
                                 )
    email = models.EmailField(_('email address'), unique=True, error_messages={
        'unique': ('A user with that email already exists.'),
    })
    phone = PhoneNumberField(
        _('phone number'), unique=True,
        blank=True, null=True, max_length=27)
    role = models.CharField(_('Role'), max_length=17, choices=Role_choices)

    is_active = models.BooleanField(_('active'), default=False)
    is_admin = models.BooleanField(_('admin'), default=False)
    is_staff = models.BooleanField(_('staff'), default=False)
    timestamp = models.DateTimeField(_("timestamp"), auto_now_add=True)

    def __str__(self):
        return self.username

    objects = CustomerManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def staff(self):
        return self.staff

    @property
    def active(self):
        return self.active

    @property
    def admin(self):
        return self.admin


class Profile(models.Model):
    gender_choices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    bio = models.TextField(_('bio'), blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics', default="default.png")
    id_no = models.CharField(
        _('National ID'), max_length=58, blank=True, null=True
    )
    nationality = CountryField(
        _("Country"), max_length=57, blank_label=('Select Country'), default='KE'
    )
    town = models.CharField(_("town"), max_length=57, blank=True, null=True)
    estate = models.CharField(
        _('estate'), max_length=57, blank=True, null=True
    )
    gender = models.CharField(_('gender'), choices=gender_choices,
                              max_length=20, default="Male"
                              )
    date_of_birth = models.DateField(_('date of birth'), blank=True, null=True)
    timestamp = models.DateTimeField(_("timestamp"), auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        abstract = True


class Administrator(Profile):
    job_id = models.CharField(
        _("Job id no"), max_length=30, blank=True, null=True
    )
    available = models.BooleanField(_("available"), default=False)

    def __str__(self):
        return self.user.username


class Student(Profile):
    admission_no = models.CharField(
        _("student id"), max_length=30,
        unique=True, blank=True, null=True
    )
    course = models.ForeignKey(
        'Course', on_delete=models.DO_NOTHING,
        blank=True, null=True)

    def __str__(self):
        return self.user.username


class Course(TrackingModel):
    course_name = models.CharField(_('course name'),
                                   max_length=257)
    code = models.CharField(_("code"), max_length=47,
                            unique=True)
    duration = models.CharField(_("duration"), max_length=15)
    date_started = models.DateField(_("date started"), null=True)
    completion_date = models.DateField(_("completion date"),
                                       null=True)
    added_by = models.ForeignKey(Administrator, on_delete=models.DO_NOTHING,
                                 blank=True, null=True)

    def __str__(self):
        return self.course_name

    class Meta:
        verbose_name_plural = "Courses"
        ordering = ["-id"]
