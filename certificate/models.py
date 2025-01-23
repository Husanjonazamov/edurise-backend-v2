from django.db import models
from organization.models import Course
from user.models import User
import helpers.permissions as permissions

from django.core.exceptions import ValidationError
from PIL import Image


def validate_image_dimensions(image):
    img = Image.open(image)
    width, height = img.size
    if width != 3264 or height != 2308:
        raise ValidationError(f"Image dimensions should be 800x600 pixels. Current dimensions are {width}x{height}.")


class CertificateTemplates(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='certificate_image/', validators=[validate_image_dimensions])
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE, related_name='certificate_templates', null=True)
    
    def __str__(self) -> str:
        return self.name


class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates')
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE, related_name='certificate_list', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    certificate = models.ImageField(upload_to='certificate_image/')
    permission_classes = [permissions.IsTeacherOrReadOnly]

    def __str__(self) -> str:
        return self.user
    
    

class FastCertificate(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    course = models.CharField(max_length=250)
    certificate = models.FileField(upload_to="fast-certificates/")
    create_at = models.DateTimeField(auto_now_add=True)
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE, related_name='fast_certificate_list', null=True)

    class Meta:
        ordering = ['-create_at']