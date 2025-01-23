from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from . import models




class CertificateTemplatesSerializer(ModelSerializer):
    class Meta:
        model = models.CertificateTemplates
        fields = '__all__'
        
        

class CertificateSerializer(ModelSerializer):
    template = PrimaryKeyRelatedField(queryset=models.CertificateTemplates.objects.all())
    
    class Meta:
        model = models.Certificate
        fields = [
            'id',
            'user',
            'template',
            'course',
        ]


class FastCertificateSerializer(ModelSerializer):
    class Meta:
        model = models.FastCertificate
        fields = '__all__'