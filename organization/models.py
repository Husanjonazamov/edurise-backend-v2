from django.db import models
from user.models import User


class Room(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']


class Area(models.Model):
    title = models.CharField(max_length=250)
    create_at = models.DateField(auto_now_add=True)
  
    def __str__(self) -> str:
        return self.title



class ThemeImages(models.Model):
    image = models.ImageField(upload_to='theme_images')

    def __str__(self):
        return self.image.url.split('/')[-1]
    
    
    
class Theme(models.Model):
    title = models.CharField(max_length=250, default='Yangi mavzu')
    content = models.JSONField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title



class Course(models.Model):
    days_choice = (
        ('Toq kunlari', 'Toq kunlari'),
        ('Juft kunlari', 'Juft kunlari'),
    )
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    start_at = models.TimeField()
    end_at = models.TimeField()
    open_at = models.DateField(auto_now_add=True)
    close_at = models.DateField()
    days = models.CharField(choices=days_choice, default='Juft kunlari', max_length=20)
    students = models.ManyToManyField(User, related_name='student_courses', blank=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_courses')
    price = models.IntegerField()
    index = models.PositiveIntegerField(default=0)
    themes = models.ManyToManyField(Theme, related_name='course_themes', blank=True)
    

class Homework(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=False)
    status = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return str(self.student)

class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=False)
    status = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return str(self.student)


class Variant(models.Model):
    variant = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.variant
    
    

class Question(models.Model):
    question = models.TextField()
    options = models.ManyToManyField(Variant, related_name='question_options')
    answer = models.ForeignKey(Variant, related_name='question_answer', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return self.question



class Quiz(models.Model):

    TIME_CHOICES = [
        ('05:00', '05:00'),
        ('10:00', '10:00'),
        ('15:00', '15:00'),
        ('20:00', '20:00'),
        ('25:00', '25:00'),
        ('30:00', '30:00'),
        ('35:00', '35:00'),
        ('40:00', '40:00'),
        ('45:00', '45:00'),
    ]
    
    poster = models.ImageField(upload_to='quiz_poster/')
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    time = models.CharField(choices=TIME_CHOICES, max_length=10)
    dificulty = models.CharField(max_length=100)
    description = models.TextField()
    questions = models.ManyToManyField(Question)
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE, related_name='quizzes', null=True, blank=True)
    
    def __str__(self) -> str:
        return self.name
    


class QuizResult(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user


        
class Organization(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='organization_logo/')
    courses = models.ManyToManyField(Course, blank=True)
    rooms = models.ManyToManyField(Room, blank=True)
    moderator = models.ForeignKey(User, related_name='moderator_organization', on_delete=models.CASCADE, default=None, null=True)
    teachers = models.ManyToManyField(User, related_name='teacher_organization', blank=True)
    students = models.ManyToManyField(User, related_name='student_organization', blank=True)
    certificates = models.ManyToManyField('certificate.Certificate', related_name='organization_certificates', blank=True)
    areas = models.ManyToManyField(Area, blank=True)
    quizes  = models.ManyToManyField(Quiz, related_name='organization_quizzes', blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.name
