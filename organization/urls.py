from django.urls import path
from . import views

urlpatterns = [
    
    # organization
    path('', views.OrganizationListCreateAPIView.as_view()),
    path('<int:pk>', views.OrganizationRetrieveUpdateDestroyAPIView.as_view()),

    # teachers
    path('teachers/', views.TeacherListGlobalApiView.as_view()),
    path('<int:pk>/teachers/', views.TeacherListInOrganizationApiView.as_view()),
    path('<int:pk>/teachers/<int:teacher_pk>/set-organization/', views.AddTeacherToOrganization.as_view()),

    # organization student
    path('<int:pk>/students/', views.OrganizationStudentsListCreateAPIView.as_view()),
    path('<int:pk>/students/<str:student_username>/get-auth-data/', views.GetStudentLogin.as_view()),

    # rooms
    path('<int:pk>/rooms/', views.RoomListCreateAPIView.as_view()),
    path('<int:pk>/rooms/<int:room_pk>/', views.RoomRetrieveUpdateDestroyAPIView.as_view()),

    # areas
    path('<int:pk>/areas/', views.AreaListCreateAPIView.as_view()),
    path('<int:pk>/areas/<int:area_pk>/', views.AreaRetrieveUpdateDestroyAPIView.as_view()),

    # courses
    path('<int:pk>/course/', views.CourseListCreateAPIView.as_view()),
    path('<int:pk>/course/<int:course_pk>', views.CourseRetrieveUpdateDestroyAPIView.as_view()),
    path('<int:pk>/course/<int:course_pk>/students', views.CourseStudentListAPIView.as_view()),
    path('<int:pk>/course/<int:course_pk>/students/add-student/<int:student_pk>', views.AddStudentToCourseAPIView.as_view()),
    path('<int:pk>/course/<int:course_pk>/students/remove-student/<int:student_pk>', views.RemoveStudentToCourseAPIView.as_view()),
    path('<int:pk>/course/<int:course_pk>/performance/', views.CoursePerformanceAPIView.as_view()),

    # attendance
    path('<int:pk>/course/<int:course_pk>/attendance/<str:student_username>', views.StudentAttendance.as_view()),

    # homework
    path('<int:pk>/course/<int:course_pk>/homework/<str:student_username>', views.StudentHomework.as_view()),

    # theme
    path('<int:pk>/course/<int:course_pk>/themes/', views.ThemeListAPIView.as_view()),
    path('<int:pk>/course/<int:course_pk>/themes/<int:theme_pk>', views.ThemeRetrieveUpdateAPIView.as_view()),
    path('<int:pk>/course/<int:course_pk>/themes/this-day/', views.ThisDayThemeRetrieveUpdateAPIView.as_view()),

    # quiz
    path('<int:pk>/quiz/', views.QuizListCreateAPIView.as_view()),
    # path('<int:pk>/quiz/<int:quiz_pk>', views.QuizRetrieveUpdateDestroyAPIView.as_view()),
]