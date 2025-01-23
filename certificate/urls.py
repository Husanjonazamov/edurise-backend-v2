from django.urls import path
from . import views

urlpatterns = [
    path('organization/<int:organization_id>/templates/', views.CertificateTemplatesListCreateAPIView.as_view()),
    path('organization/<int:organization_id>/templates/<int:pk>', views.CertificateRetrieveUpdateDestroyAPIView.as_view()),
    path('organization/<int:organization_id>/certificates/', views.CertificateListCreateAPIView.as_view()),

    # fast certificates
    path('organization/<int:organization_id>/fast-certificates/create/', views.FastCertificateGenerateView.as_view()),
    path('organization/<int:organization_id>/fast-certificates/list/', views.FastCertificatesListAPIView.as_view()),
]
