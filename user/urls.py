from django.urls import path

from . import views

urlpatterns = [

    # auth urls
    path('auth/send-code/', views.SendCodeAPIView.as_view()),
    path('auth/confirm-code/', views.ConfirmCodeAPIView.as_view()),

    # update
    path('update/', views.UserUpdateAPIView.as_view()),

    # get me
    path('get-me/', views.GetMeAPIView.as_view()),
]
