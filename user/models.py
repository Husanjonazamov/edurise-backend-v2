from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin

from user.usermanager import ConfirmedUsersManager
import helpers.permissions as permissions

# Create your models here.

LANG_CHOICE = (
    ('uz', 'uz'),
    ('ru', 'ru'),
    ('en', 'en'),
    ('cr', 'cr'),
)


class StudentLogin(models.Model):
    student = models.ForeignKey('User', on_delete=models.CASCADE)
    password = models.CharField(max_length=250)

    def __str__(self):
        return str(self.student)


class User(AbstractUser, PermissionsMixin):
    role_choices = (
        ('moderator', 'moderator'),
        ('teacher', 'teacher'),
        ('student', 'student'),
    )

    first_name = models.CharField(max_length=250, null=True, blank=True)
    last_name = models.CharField(max_length=250, null=True, blank=True)
    pic = models.ImageField(upload_to='avatars/', null=True, blank=True)
    role = models.CharField(choices=role_choices, max_length=25, null=True, blank=True)
    lang = models.CharField(choices=LANG_CHOICE, max_length=5, default='uz')
    inherint = models.PositiveIntegerField(unique=True, null=True, blank=True)

    objects = ConfirmedUsersManager()

    # SMTP user models
    status_choice = (
        ('unconfirmed', 'unconfirmed'),
        ('confirmed', 'confirmed'),
        ('verified', 'verified'),
    )

    code = models.PositiveIntegerField(null=True, blank=True)
    code_creation_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    status = models.CharField(choices=status_choice, max_length=100, null=True, blank=True, default='unconfirmed')

    permission_classes = [permissions.IsModeratorOrReadOnly]

    class Meta:
        ordering = ('role',)

    def __str__(self):
        return f"{self.username}: {self.first_name} {self.last_name}"
