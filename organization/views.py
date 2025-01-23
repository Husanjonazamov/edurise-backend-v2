from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework.filters import OrderingFilter

from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend

from helpers.is_day import isDayPairOrEvenCheck

from .models import *
from user.serializers import *
from .serializers import *

from helpers.permissions import * 
# Create your views here.


class OrganizationListCreateAPIView(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsModeratorOrIsTeacher]

    def get_queryset(self):
        request_user_role = self.request.user.role
        if(request_user_role == 'moderator'):
            organizations = Organization.objects.filter(moderator=self.request.user)
        elif request_user_role == 'teacher':
            organizations = Organization.objects.filter(teachers=self.request.user)

        return organizations
    
    

class OrganizationRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsModeratorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(moderator=self.request.user)


class OrganizationStudentsListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsModeratorOrIsTeacherOrReadOnly] 
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'username',
        'first_name',
        'last_name',
    ]

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        organization = get_object_or_404(Organization, pk=pk)
        students = organization.students.all()
        return students
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        organization = get_object_or_404(Organization, pk=pk)
        student = serializer.save()
        organization.students.add(student)
        return super().perform_create(serializer)

class GetStudentLogin(APIView):
    permission_classes = [IsModeratorOrIsTeacherOrReadOnly]

    def get(self, request, pk, student_username):
        organization = get_object_or_404(Organization, pk=pk)
        student = get_object_or_404(organization.students, username=student_username)
        auth = get_object_or_404(StudentLogin, student=student)

        return Response({
            'username': student_username,
            'password': auth.password
        })
        
    
class RoomListCreateAPIView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsModeratorOrReadOnly]
    
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        organization = get_object_or_404(Organization, pk=pk)
        rooms = organization.rooms.all()
        return rooms
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        organization = get_object_or_404(Organization, pk=pk)
        room = serializer.save(organization=organization)
        organization.rooms.add(room)
        return super().perform_create(serializer)


class RoomRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsModeratorOrReadOnly]
    
    def get_object(self):
        pk = self.kwargs.get('pk')
        room_pk = self.kwargs.get('room_pk')
        organization = get_object_or_404(Organization, pk=pk)
        room = get_object_or_404(organization.rooms, pk=room_pk)
        return room   


class AreaListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = AreaSerializer
    permission_classes = [IsModeratorOrReadOnly]
    
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        organization = get_object_or_404(Organization, pk=pk)
        areas = organization.areas.all()
        return areas
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        organization = get_object_or_404(Organization, pk=pk)
        area = serializer.save()
        organization.areas.add(area)
        return super().perform_create(serializer)


class AreaRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AreaSerializer
    permission_classes = [IsModeratorOrReadOnly]

    def get_object(self):
        pk = self.kwargs.get('pk')
        area_pk = self.kwargs.get('area_pk')
        organization = get_object_or_404(Organization, pk=pk)
        area = get_object_or_404(organization.areas, pk=area_pk)
        return area


class CourseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsModeratorOrReadOnly]

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        organization = get_object_or_404(Organization, pk=pk)
        courses = organization.courses.all()
        return courses

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        organization = get_object_or_404(Organization, pk=pk)

        if serializer.is_valid():    
            course = serializer.save(
                organization=organization,
                index=organization.courses.count() + 1
                )
        
        organization.courses.add(course)
        return super().perform_create(serializer)


class CourseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsModeratorOrReadOnly]

    def get_object(self):
        pk = self.kwargs.get('pk')
        course_pk = self.kwargs.get('course_pk')
        organization = get_object_or_404(Organization, pk=pk)
        course = get_object_or_404(organization.courses, pk=course_pk)
        return course


class CourseStudentListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsModeratorOrIsTeacherOrReadOnly]

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        course_pk = self.kwargs.get('course_pk')
        organization = get_object_or_404(Organization, pk=pk)
        course = get_object_or_404(organization.courses, pk=course_pk)
        students = course.students.all()
        return students


class CoursePerformanceAPIView(APIView):
    
    def get(self, request, pk, course_pk):
        organization = get_object_or_404(Organization, pk=pk)
        course = get_object_or_404(organization.courses, pk=course_pk)

        arrived_attendance = Attendance.objects.filter(course=course, status=True).count()
        notcome_attendance = Attendance.objects.filter(course=course, status=False).count()
        
        succes_homework = Homework.objects.filter(course=course, status=True).count()
        unfulfilled_homework = Homework.objects.filter(course=course, status=False).count()

        succes_themes = course.themes.filter(content__isnull=False).count()
        unfulfilled_themes = course.themes.filter(content__isnull=True).count()

        return Response({
            'theme': {
                'success': succes_themes,
                'unfulfilled': unfulfilled_themes,
                "total": succes_themes + unfulfilled_themes
                },
            'attendance':{
                'arrived':arrived_attendance,
                'notcome':notcome_attendance,
                'total': arrived_attendance + notcome_attendance
            },
            'homework':{
                'success':succes_homework,
                'unfulfilled':unfulfilled_homework,
                'total': succes_homework + unfulfilled_homework
            }
        })
        

class AddStudentToCourseAPIView(APIView):

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        course_pk = self.kwargs.get('course_pk')
        student_pk = self.kwargs.get('student_pk')
        
        # Tashkilot, kurs va talaba obyektlarini olish
        organization = get_object_or_404(Organization, pk=pk)
        course = get_object_or_404(organization.courses, pk=course_pk)
        student = get_object_or_404(organization.students, pk=student_pk)

        # Tashkilot va kursga talabani qo'shish
        course.students.add(student)

        return Response(status=status.HTTP_201_CREATED)
            
        
class RemoveStudentToCourseAPIView(APIView):

    def delete(self, request, pk, course_pk, student_pk):
        organization = get_object_or_404(Organization, pk=pk)
        course = get_object_or_404(organization.courses, pk=course_pk)
        student = get_object_or_404(User, pk=student_pk)

        organization.students.remove(student)
        course.students.remove(student)
        
        return Response(status=status.HTTP_204_NO_CONTENT)


class StudentAttendance(APIView):

    def get(self, request, pk, course_pk, student_username):
        organization = get_object_or_404(Organization, pk=pk)
        course = get_object_or_404(organization.courses, pk=course_pk)
        student = get_object_or_404(User, username=student_username)

        course_days = course.days
        isDay = isDayPairOrEvenCheck(course_days)
        
        comes = Attendance.objects.filter(
            student = student,
            course = course,
            status = True
        )
        
        
        if not isDay:
            return Response({
                'comes': comes.count(),
                'status': None
            })
        
        day = timezone.now()
        
        attendance = Attendance.objects.get_or_create(
            student = student,
            course = course,
            date = day
        )[0]

        Homework.objects.get_or_create(
            student = student,
            course = course,
            date = day,
        )
        
        return Response({
            'status': attendance.status,
            'comes': comes.count()
        })
        
    def put(self, request, pk, course_pk, student_username):
        organization = get_object_or_404(Organization, pk=pk)
        course = get_object_or_404(organization.courses, pk=course_pk)
        student = get_object_or_404(User, username=student_username)
        
        attendance = get_object_or_404(
            Attendance,
            student = student,
            course = course,
            date = timezone.now()
        )

        attendance.status = not attendance.status
        attendance.save()
        
        return Response(
            data = {
                'status':attendance.status
            },
            status=status.HTTP_200_OK
        )


class ThemeListAPIView(generics.ListAPIView):
    serializer_class = ThemeSerializer

    def get_queryset(self):

        pk = self.kwargs.get('pk')
        course_pk = self.kwargs.get('course_pk')
        
        organization = get_object_or_404(Organization, pk=pk)
        course = get_object_or_404(organization.courses, pk=course_pk)

        return course.themes.all()



class ThemeRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ThemeCreateSerializer

    def get_object(self):
        
        pk = self.kwargs.get('pk')
        course_pk = self.kwargs.get('course_pk')
        
        organization = get_object_or_404(Organization, pk=pk)
        course = get_object_or_404(organization.courses, pk=course_pk)

        theme = get_object_or_404(course.themes, pk=self.kwargs.get('theme_pk'))
        return theme
    
        
class ThisDayThemeRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ThemeCreateSerializer
    
    def get_object(self):
        
        pk = self.kwargs.get('pk')
        course_pk = self.kwargs.get('course_pk')
        
        organization = get_object_or_404(Organization, pk=pk)
        course = get_object_or_404(organization.courses, pk=course_pk)

        if not isDayPairOrEvenCheck(course.days):
            raise serializers.ValidationError({
                'status': 'error',
                'message': 'Bugungi dars kuni emas'
            })

        theme = Theme.objects.get_or_create(
            created_at = timezone.now(),
        )[0]
        
        course.themes.add(theme)

        return theme




class StudentHomework(APIView):

    def get(self, request, pk, course_pk, student_username):
        organization = get_object_or_404(Organization, pk=pk)
        course = get_object_or_404(organization.courses, pk=course_pk)
        student = get_object_or_404(User, username=student_username)

        day = timezone.now()
        homework = Homework.objects.filter(
            student = student,
            course = course,
            date = day,
        ).first()

        if homework is None:
            return Response({
                'status': None
            })
        return Response({
            'status': homework.status
        })
        
    def put(self, request, pk, course_pk, student_username):
        organization = get_object_or_404(Organization, pk=pk)
        course = get_object_or_404(organization.courses, pk=course_pk)
        student = get_object_or_404(User, username=student_username)
        
        day = timezone.now()
        
        homework = Homework.objects.get(
            student = student,
            course = course,
            date = day,
        )
        homework.status = not homework.status
        homework.save()

        return Response(
            data = {
                'status':homework.status
            },
            status=status.HTTP_200_OK
        )


class QuizListCreateAPIView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsModeratorOrReadOnly]
    
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        organization = get_object_or_404(Organization, pk=pk)
        quizes = organization.quizes.all()

        return quizes

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        organization = get_object_or_404(Organization, pk=pk)    
        quiz = serializer.save(
            organization=organization
        )

        organization.quizes.add(quiz)


class TeacherListGlobalApiView(generics.ListAPIView):
    queryset = User.objects.filter(role='teacher', first_name__isnull=False, last_name__isnull=False, pic__isnull=False)
    serializer_class = UserSerializer
    permission_classes = [IsModeratorOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = [
            'id',
            'first_name',
            'last_name',
        ]


class TeacherListInOrganizationApiView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsModeratorOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        organization = get_object_or_404(Organization, pk=pk)
        teachers = organization.teachers.all()
        return teachers

class AddTeacherToOrganization(APIView):
    
    def post(self, request, pk, teacher_pk):
        organization = get_object_or_404(Organization, pk=pk)
        teacher = get_object_or_404(User, username=teacher_pk)

        organization.teachers.add(teacher)
        
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk, teacher_pk):
        organization = get_object_or_404(Organization, pk=pk)
        teacher = get_object_or_404(User, username=teacher_pk)

        organization.teachers.remove(teacher)
        
        return Response(status=status.HTTP_204_NO_CONTENT)