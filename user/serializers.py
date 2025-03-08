from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = '__all__'


class ServicesProvidedSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServicesProvided
        fields = '__all__'

class PreferenceAreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = PreferenceArea
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'

class ExperienceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Experience
        fields = '__all__'


class WorkerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Worker
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields = ("id","username","first_name","last_name","email")