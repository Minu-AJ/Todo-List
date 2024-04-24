from django.db import models
from django.contrib.auth.models import User

# User>>AbstractBaseUser>>BaseUser

class Taskmodel(models.Model):
    
    task_name=models.CharField(max_length=100)
    task_description=models.TextField()
    created_date=models.DateField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    completed=models.BooleanField(default=False)