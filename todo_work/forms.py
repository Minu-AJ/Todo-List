from django import forms
from todo_work.models import User,Taskmodel

class Register(forms.ModelForm):
    
    class Meta:
        
        model=User
        fields=['username','first_name','last_name','email','password']
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}),
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}),
            'password':forms.TextInput(attrs={'class':'form-control','placeholder':'Password'})
        }
        
        
class TaskForm(forms.ModelForm):
    
    class Meta:
        
        model=Taskmodel
        fields=['task_name','task_description']
        widgets={
            'task_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Task Name'}),
            'task_description':forms.Textarea(attrs={'class':'form-control','column':20,'row':5,'placeholder':'Task Description'})
        }
        

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))

        
        