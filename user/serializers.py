from rest_framework import serializers

from helpers.randomizer import generate_random_password, generate_random_username
from .models import *

class StudentLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentLogin
        fields = '__all__'



class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)
    username = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'role',
            'pic',
            'lang',
            'inherint',
            'status',
            'username'
        ]
        depth = 2

    def create(self, validated_data):
        password = generate_random_password(8)

        student = User.objects.create_user(
            username=generate_random_username(user=User, length=5),
            password=password,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            status='confirmed',
            role='student'
        )

        StudentLogin.objects.create(student=student, password=password)
        
        return student