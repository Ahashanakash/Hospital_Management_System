from rest_framework import serializers
from . import models
from django.contrib.auth.models import User

class PatientSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    class Meta:
        model = models.Patient
        fields = '__all__'
        
class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True, write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        
        if password != confirm_password:
            raise serializers.ValidationError({'error': "Password Doesn't Match"})
        
        return data
    
    def create(self, validated_data):
        # Remove confirm_password from validated_data before creating User
        validated_data.pop('confirm_password', None)
        
        username = validated_data['username']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        email = validated_data['email']
        password = validated_data['password']
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': "Email Already exists"})
        
        account = User(
            username=username, 
            email=email, 
            first_name=first_name, 
            last_name=last_name
        )
        account.set_password(password)
        account.is_active = False
        account.save()
        return account
        
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)