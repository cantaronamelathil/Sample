from rest_framework import serializers
from .models import UserModel
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id','username','password','email','role','profile_image']
        read_only_field = ['id','username','role']        
    def create(self,validated_data):
        password = validated_data.pop('password')
        user = UserModel(**validated_data)
        user.set_password(password)
        user.save()
        return user    
        
class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)   
    
    class Meta:
        model = UserModel
        fields = ['username','password'] 
             
             
    def validate(self,data):
        user = authenticate(username = data ['username'], password = data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid username or password")
        if not user.is_active:
            
            raise serializers.ValidationError("Invalid credentials")
        return user
             
             
             
class BlockUserSerializer(serializers.ModelSerializer):
        class Meta:
            model = UserModel
            fields = ['is_active']
            extra_kwargs = {
                'is_active':{'required':True}
                
            }             
            