from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from api.serializers import Registration,User,Todoserializer
from rest_framework import status
from todo_work.models import Taskmodel

from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework import authentication, permissions
from api.permissions import OwnerOnly


class Userregister(APIView):
    
    def post(self,request,*args,**kwargs):
        
        serializer=Registration(data=request.data)
        
        if serializer.is_valid():
            
            serializer.save()
            
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    
class Todoviewsetview(ViewSet):
    
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    
    def list(self,request,*args,**kwargs):
        
        qs=Taskmodel.objects.all()
        
        serializer=Todoserializer(qs,many=True)
        
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    
    def create(self,request,*args,**kwargs):
        
        serializer=Todoserializer(data=request.data)
        
        if serializer.is_valid():
            
            serializer.save(user=request.user)
            
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        else:
            
            return Response(serializer.errors,status=status.HTTP_403_FORBIDDEN)
        
    
    def destroy(self,request,*args,**kwargs):
        
        id=kwargs.get("pk")
        
        qs=Taskmodel.objects.get(id=id)
        
        if qs.user==request.user:
            
            qs.delete()
        
            return Response({"message":"Todo object deleted"})
        
        else:
            
            raise serializers.ValidationError("not allowed")
            # or >>> return Response({"message":"not allowed"})
    
    
    def update(self,request,*args,**kwargs):
        
        id=kwargs.get("pk")
        
        qs=Taskmodel.objects.get(id=id)
        
        serializer=Todoserializer(data=request.data,instance=qs)
            
        if serializer.is_valid():
            
            serializer.save()
            
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        else:
            
            return Response(serializer.errors,status=status.HTTP_304_NOT_MODIFIED)
            

    
    def retrieve(self,request,*args,**kwargs):
        
        id=kwargs.get("pk")
        
        qs=Taskmodel.objects.get(id=id)
        
        serializer=Todoserializer(qs)
                
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    
    
# ModelViewset

class Todomodelviewset(ModelViewSet):
    
    queryset=Taskmodel.objects.all()
    serializer_class=Todoserializer
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[OwnerOnly]
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
        