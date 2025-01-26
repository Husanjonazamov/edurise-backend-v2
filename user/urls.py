from django.urls import path
from . import views

urlpatterns = [

    # update
    path('update/', views.UserUpdateAPIView.as_view()),

    # get me
    path('get-me/', views.GetMeAPIView.as_view()),
]
