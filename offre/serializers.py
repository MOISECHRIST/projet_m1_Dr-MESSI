from rest_framework import serializers
from .models import *

class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = '__all__'

class MediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Media
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'

class WorkerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Worker
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = '__all__'


class WorkOfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkOffer
        fields = '__all__'


class OfferApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfferApplication
        fields = '__all__'