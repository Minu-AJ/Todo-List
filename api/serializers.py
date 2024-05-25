from rest_framework import serializers
from todo_work.models import User, Taskmodel


class Registration(serializers.ModelSerializer):
    
    class Meta:
        
        model=User
        
        fields=['id','username','email','password','first_name','last_name']
        
        read_only_fields=['id']
        
    def create(self, validated_data):
        
        return User.objects.create_user(**validated_data) 


class Todoserializer(serializers.ModelSerializer):
    
    user=serializers.StringRelatedField(read_only=True)
    
    class Meta:
        
        model=Taskmodel
        
        fields="__all__"
        
        read_only_fields=['id','created_date','user','completed']