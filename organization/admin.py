from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Organization)
admin.site.register(models.Course)
admin.site.register(models.Area)
admin.site.register(models.Room)
admin.site.register(models.Attendance)
admin.site.register(models.Variant)
admin.site.register(models.Question)
admin.site.register(models.Quiz)
admin.site.register(models.QuizResult)
admin.site.register(models.Theme)