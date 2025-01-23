from rest_framework import serializers

from helpers.is_day import isDayPairOrEvenCheck
from .models import *

class OrganizationSerializer(serializers.ModelSerializer):

    total_income = serializers.SerializerMethodField()
    total_students = serializers.SerializerMethodField()
    total_teachers = serializers.SerializerMethodField()
    
    def get_total_income(self, obj):
        courses = obj.courses.all()
        total_ammount = 0
        
        for i in courses:
            total_ammount += i.price
        
        return total_ammount
    def get_total_students(self, obj):
        students_count = obj.students.all().count()        
        return students_count

    def get_total_teachers(self, obj):
        teachers_count = obj.teachers.all().count()        
        return teachers_count
    
    class Meta:
        model = Organization
        fields = (
            'id', 'total_income', 'total_students', 'total_teachers', 'name', 'logo', 'create_at',
        )

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user

        attrs['moderator'] = user
        
        return super().validate(attrs)
    
    def get_fields(self):
        fields = super().get_fields()
        
        # Misol uchun, agar requestda "show_extra" query parametri mavjud bo'lsa, qo'shimcha maydonlarni qo'shamiz
        request = self.context.get('request')
        request_method = request.method if request else None
        
        fields.pop('moderator', None)

        return fields
    
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        organizations = Organization.objects.filter(moderator=user)
        organizations_count = organizations.count()

        if organizations_count >= 3:
                raise serializers.ValidationError({'error': 'You have already reached the maximum number of organizations (3).'})
        return super().create(validated_data)

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"


class ThemeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ['id', 'title', 'content', 'created_at', 'updated_at']
    

    
class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ['id', 'title', 'content', 'created_at', 'updated_at']

    
    def get_fields(self):
        fields = super().get_fields()
        
        request = self.context.get('request')
        request_method = request.method if request else None
        
        if request_method == 'GET':
            fields.pop('content', None)

        return fields

    

class AreaSerializer(serializers.ModelSerializer):

    total_courses = serializers.SerializerMethodField()
    total_income = serializers.SerializerMethodField()
    
    def get_total_courses(self, obj):
        return Course.objects.filter(area=obj).count()

    def get_total_income(self, obj):
        
        courses = Course.objects.filter(area=obj)
        total_ammount = 0
        
        for i in courses:
            total_ammount += i.price
        
        return total_ammount
    
    class Meta:
        model = Area
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    teacher = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    area = serializers.PrimaryKeyRelatedField(queryset=Area.objects.all())
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
    total_price = serializers.SerializerMethodField()
    
    def get_total_price(self, obj):
        return obj.price * obj.students.count()
    
    class Meta:
        model = Course
        fields = "__all__"
        depth = 1
    
    def to_representation(self, instance):
        """Customize the serialization to include teacher details"""
        representation = super().to_representation(instance)
        teacher = instance.teacher
        area = instance.area
        room = instance.room
        pic = self.context.get('request').build_absolute_uri(teacher.pic.url)
        representation['room'] = {
            "id": room.id,
            "name": room.name,
            "capacity": room.capacity,
        }
        if teacher:
            representation['teacher'] = {
                'id': teacher.id,
                'first_name': teacher.first_name,
                'last_name': teacher.last_name,
                'pic': pic,
            }

        if area:
            representation['area'] = {
                'id': area.id,
                'title': area.title
            }

        representation.pop('students', None)
        

        return representation


# ========= QUIZ ==============

class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = ['id', 'variant']

class QuestionSerializer(serializers.ModelSerializer):
    options = VariantSerializer(many=True)
    answer = serializers.CharField(max_length=250)
    depth = 2
    
    class Meta:
        model = Question
        fields = ['id', 'question', 'options', 'answer']

    def create(self, validated_data):
        
        answer = validated_data.get('answer')
        del validated_data['answer']
        
        options_data = validated_data.pop('options', [])
        question = Question.objects.create(
            **validated_data
        )
        for option_data in options_data:
            new_option = Variant.objects.create(
                variant=option_data['variant'],
            )
            question.options.add(new_option)

        answer = question.options.get(variant=answer)
        question.answer = answer
        question.save()

        return question

    def update(self, instance, validated_data):
        options_data = validated_data.pop('options', [])
        instance.question = validated_data.get('question', instance.question)
        instance.save()

        # Clear existing options and create new ones
        instance.options.clear()
        for option_data in options_data:
            Variant.objects.create(question=instance, **option_data)

        return instance

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    
    class Meta:
        model = Quiz
        fields = ['poster', 'id', 'title', 'description', 'questions', 'area', 'organization', 'time']
    
    def to_representation(self, instance):
        requests = self.context['request']

        if requests.method == 'GET':
            data = super().to_representation(instance)
            data.pop('questions')

            data['author'] = 'salom'
            
            return data
        return super().to_representation(instance)
    
    def create(self, validated_data):
        questions_data = validated_data.pop('questions', [])
        quiz = Quiz.objects.create(author=self.context['request'].user, **validated_data)

        for question_data in questions_data:
            question = QuestionSerializer().create(question_data)
            quiz.questions.add(question)

        return quiz


    def update(self, instance, validated_data):
        questions_data = validated_data.pop('questions', [])
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.area = validated_data.get('area', instance.area)
        instance.organization = validated_data.get('organization', instance.organization)
        instance.save()

        # Handle updating or creating questions
        for question_data in questions_data:
            question_id = question_data.get('id')
            if question_id:
                question = Question.objects.get(id=question_id)
                QuestionSerializer().update(question, question_data)
            else:
                question = QuestionSerializer().create(question_data)
            instance.questions.add(question)

        return instance

