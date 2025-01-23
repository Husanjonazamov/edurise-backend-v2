import os

from django.http import HttpRequest
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from organization.models import Organization
from . import serializers, models
from helpers.certificate import Certificate as CertificateGenerator


class CertificateTemplatesListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.CertificateTemplatesSerializer
    pagination_class = None
    
    def perform_create(self, serializer):
        organization_id = self.kwargs.get('organization_id')

        organization = get_object_or_404(Organization, id=organization_id)

        templatest = models.CertificateTemplates.objects.filter(organization=organization)
        if templatest.count() >= 3:
            raise APIException({'error': 'You can have only 3 templates'})
        
        serializer.save(
            organization=organization
        )
        return super().perform_create(serializer)
    
    def get_queryset(self):
        organization_id = self.kwargs.get('organization_id')
        organization = get_object_or_404(Organization, id=organization_id)
        organization_templates = models.CertificateTemplates.objects.filter(organization=organization)
        
        return organization_templates




class CertificateRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.CertificateTemplatesSerializer

    def get_queryset(self):
        organization_id = self.kwargs.get('organization_id')
        organization = get_object_or_404(Organization, id=organization_id)
        organization_certificates_templates = models.CertificateTemplates.objects.filter(organization=organization)
        return organization_certificates_templates





class CertificateListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.CertificateSerializer

    def get_queryset(self):
        organization_id = self.kwargs.get('organization_id')
        organization = get_object_or_404(Organization, id=organization_id)
        organization_certificates = models.Certificate.objects.filter(organization=organization)
        return organization_certificates
    
    def perform_create(self, serializer):
        organization_id = self.kwargs.get('organization_id')
        user_id = self.request.POST.get('user')
        course_id = self.request.POST.get('course')

        organization = get_object_or_404(Organization, id=organization_id)
        user = get_object_or_404(organization.students, id=user_id)
        course = get_object_or_404(organization.courses, id=course_id)

        first_name = user.first_name
        last_name = user.last_name
        
        c = CertificateGenerator()
        
        filepath, filename = c.generate(
            request=self.request,
            course=course,
            FIO=f"{first_name} {last_name}",
            color=(0, 0, 0),
            complate="kursini muvaffaqiyatli yakunladi"
        )
        
        serializer.save(
            organization=organization,
            certificate = open(filepath, 'rb')
        )   
        return super().perform_create(serializer)






class FastCertificateGenerateView(APIView):

    def post(self, request: HttpRequest, organization_id):
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", '')
        course = request.POST.get("course", '')
        template_id = request.POST.get("template_id", -1)

        organization = get_object_or_404(Organization, id=organization_id)
        template = get_object_or_404(models.CertificateTemplates, id=template_id, organization=organization)

        c = CertificateGenerator(template.image)

        print(template.image)
        print("😎 ~ views.py:95 -> template: ",  template)

        filepath, filename = c.generate(
            request=request,
            course=course,
            FIO=f"{first_name} {last_name}",
            color=(0, 0, 0),
            complate="Kursini muvaffaqiyatli yakunladi"
        )
        
        certificate = models.FastCertificate()
        certificate.first_name = first_name
        certificate.last_name = last_name
        certificate.course = course
        certificate.certificate.save(filename, open(filepath, 'rb'))
        certificate.organization = organization
        certificate.save()

        try:
            os.remove(filepath)
        except:
            pass

        certificate_absolue_url = request.build_absolute_uri(certificate.certificate.url)
        serializer_certificate = serializers.FastCertificateSerializer(certificate)
        data = serializer_certificate.data
        data['certificate'] = certificate_absolue_url
        return Response(data, status=200)




class FastCertificatesListAPIView(generics.ListAPIView):
    serializer_class = serializers.FastCertificateSerializer
    
    def get_queryset(self):
        organization_id = self.kwargs.get('organization_id')
        organization = get_object_or_404(Organization, id=organization_id)
        organization_certificates = models.FastCertificate.objects.filter(organization=organization)
        return organization_certificates
