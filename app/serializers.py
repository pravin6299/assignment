from rest_framework import serializers
from .models import Post, User
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    # def validate(self, data):
    #     username = data.get('username')
    #     password = data.get('password')

    #     user = authenticate(username=username, password=password)
    #     if not user:
    #         raise serializers.ValidationError("Incorrect credentials. Please try again.")
    #     return user
    

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title","body"]


class RetrieveSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="author.username")
    email = serializers.CharField(source="author.email")
    class Meta:
        model = Post
        fields = ["title","body","author", "username", "email"]

class GetPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields =  ["id","title","body","author"]

