from rest_framework import serializers
from . import models

class DoctorSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    # email = serializers.SerializerMethodField()
    designation = serializers.StringRelatedField(many=True)
    specialization = serializers.StringRelatedField(many=True)
    available_time = serializers.StringRelatedField(many=True)
    
    def get_first_name(self, obj):
        return obj.user.first_name if obj.user else None
    
    def get_last_name(self, obj):
        return obj.user.last_name if obj.user else None
    
    # def get_email(self, obj):
    #     return obj.user.email if obj.user else None
    
    class Meta:
        model = models.Doctor
        fields = ['id', 'first_name', 'last_name', 'image', 'designation', 'specialization', 'available_time', 'fee', 'meet_link']
class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Specialization
        fields = '__all__'
        
class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Designation
        fields = '__all__'
        
class AvailableTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AvailableTime
        fields = '__all__'
        
class ReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.SerializerMethodField()
    reviewer_image = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()
    doctor_image = serializers.SerializerMethodField()
    
    def get_reviewer_name(self, obj):
        return f"{obj.reviewer.user.first_name} {obj.reviewer.user.last_name}" if obj.reviewer and obj.reviewer.user else None
    
    def get_reviewer_image(self, obj):
        return f"{obj.reviewer.image}" if obj.reviewer and obj.reviewer.user else None
    
    def get_doctor_name(self, obj):
        return f"{obj.doctor.user.first_name} {obj.doctor.user.last_name}" if obj.doctor and obj.doctor.user else None
    
    def get_doctor_image(self, obj):
        return f"{obj.doctor.image}" if obj.doctor and obj.doctor.user else None
    
    class Meta:
        model = models.Review
        fields = ['id', 'reviewer_name', 'doctor_name','reviewer_image','doctor_image', 'body', 'created', 'rating']