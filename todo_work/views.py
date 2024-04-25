from django.shortcuts import render,redirect
from django.views.generic import View
from todo_work.forms import Register,LoginForm,TaskForm
from todo_work.models import User,Taskmodel
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils.decorators import method_decorator



def signin_required(fn):
    
    def wrapper(request,**kwargs):
        
        if not request.user.is_authenticated:
            return redirect("login")
        else:
            return fn(request,**kwargs)
    return wrapper


# check the whether the loggined user or not to perform the corresponding task
def mylogin(fn):
    
    def wrapper(request,**kwargs):
        
        id=kwargs.get("pk")
        obj=Taskmodel.objects.get(id=id)
        
        if obj.user!=request.user:
            return redirect("login")
        else:
            return fn(request,**kwargs)
    return wrapper



class Registeration(View):
    
    def get(self,request,**kwargs):
        
        form=Register()
        return render(request,"register.html",{"form":form})
    
    def post(self,request,**kwargs):
        
        form=Register(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
        form=Register()
        return redirect("login")
            

class Signin(View):
    
    def get(self,request,*kwargs):
        
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    
    def post(self,request,**kwargs):
        
        form=LoginForm(request.POST)
        
        if form.is_valid():     #username,password
            print(form.cleaned_data)
            
            u_name=form.cleaned_data.get("username")
            # getting username and password from cleaned_data
            pwd=form.cleaned_data.get("password")
            
            user_obj=authenticate(username=u_name,password=pwd)
            # checking if the username and password are valid in the table auth_user
            
            if user_obj:
                print("valid credential")
                # if true passing the user_obj to the login function
                login(request,user_obj)
                return redirect("index")
            else:
                print("incorrect credential")
                return render(request,"login.html")
            

@method_decorator(signin_required,name="dispatch")           
class Add_task(View):
    
    def get(self,request,**kwargs):
        
        form=TaskForm()
        data=Taskmodel.objects.filter(user=request.user).order_by('completed')
        return render(request,"index.html",{"form":form,"data":data})
    
    def post(self,request,**kwargs):
        
        form=TaskForm(request.POST)         
        
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            messages.success(request,"task added successfully")
        
        form=TaskForm()
        data=Taskmodel.objects.filter(user=request.user).order_by('completed')
        return render(request,"index.html",{"form":form,"data":data})

    
@method_decorator(mylogin,name="dispatch")
@method_decorator(signin_required,name="dispatch")
class Delete_task(View):
    
    def get(self,request,**kwargs):
        
        id=kwargs.get("pk")
        Taskmodel.objects.get(id=id).delete()
        return redirect("index")

    
@method_decorator(signin_required,name="dispatch")   
class Task_edit(View):
    
    def get(self,request,**kwargs):
        
        id=kwargs.get("pk")
        obj=Taskmodel.objects.get(id=id)

        if obj.completed == False:
            obj.completed = True
            obj.save()
        return redirect("index")
    
    
class Signout(View):
    
    def get(self,request):
        
        logout(request)
        return redirect("login")

    
@method_decorator(mylogin,name="dispatch")
@method_decorator(signin_required,name="dispatch")   
class User_del(View):
    
    def get(self,request,**kwargs):
        
        id=kwargs.get("pk")
        User.objects.get(id=id).delete()
        return redirect("register")
    
    
class Update_user(View):
    
    def get(self,request,**kwargs):
        
        id=kwargs.get("pk")
        data=User.objects.get(id=id)
        form=Register(instance=data)
        return render(request,"register.html",{"form":form})
    
    def post(self,request,**kwargs):
        
        id=kwargs.get("pk")
        data=User.objects.get(id=id)
        form=Register(request.POST,instance=data)
        
        if form.is_valid():
            form.save()
        return redirect("login")        



        
        

        
            
            
        
            
            
    
    