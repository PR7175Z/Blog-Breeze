from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Blog, Category
from django.shortcuts import render, redirect
import re

def indexpageloader(request):
  blogs = Blog.objects.all().order_by('-publishdate')
  template = loader.get_template('index.html')
  context = {
    'blogs': blogs,
  }
  return HttpResponse(template.render(context, request))

def bloglistingloader(request):
  blogs = Blog.objects.all().order_by('-publishdate')
  template = loader.get_template('bloglisting.html')
  context = {
    'blogs': blogs,
  }
  return HttpResponse(template.render(context, request))

def blogsingle(request, id):
  blogsingle = Blog.objects.get(id=id)
  other_blogs = Blog.objects.exclude(id=id).order_by('?')[:3]
  template = loader.get_template('blogsingle.html')
  context = {
    'blogsingle': blogsingle,
    'otherblog':other_blogs,
  }
  return HttpResponse(template.render(context, request))

def contactpageloader(request):
  template = loader.get_template('contact.html')
  return HttpResponse(template.render())

def login_view(request):
  if request.method == "POST":
    try:
      username = request.POST.get('username')
      password = request.POST.get('password')
      user = authenticate(request, username=username, password=password)
      if user is not None:
        login(request,user)
        messages.success(request, "Login Successful")
        return redirect('/dashboard')
      else:
        messages.error(request, "invalid Credential")
    except ValueError as e:
      return render(request, 'login.html')
    except Exception as e:
      messages.error(request,f"Error: {str(e)}")
      return render (request,"login.html")
  else:
    return render (request,'login.html')
  
def dashboard_view(request):
  if request.user.is_anonymous:
    return redirect('/login')
  else:
    try:
      current_user = request.user
      current_user_id = request.user.id
      messages.success(request, f'Hello {current_user} {current_user_id}')
      return render(request,"dashboard.html")
    except Exception as e:
      messages.error(request, str(e))
      return render(request,"dashboard.html")
    
def signup_view(request):
  if request.method == "POST":
    try:
      fname = request.POST.get('firstname')
      lname = request.POST.get('lastname')
      email = request.POST.get('email')
      phone = request.POST.get('phone')
      username = request.POST.get('username')
      password = request.POST.get('password')
      role = 'author'

      if role == 'author':
        is_superuser =False 
        is_author =True
        
      user = User.objects.create_user(username,email,password,is_superuser=is_superuser)
      user.first_name=fname
      user.last_name=lname
      user.email = email
      user.phone = phone
      user.is_author = is_author
      user.save()
      
      if user is not None:
        login(request,user)
        messages.success(request, "Login Successful")
        return redirect('/dashboard')
      else:
        messages.error(request, "invalid Credential")
    except ValueError as e:
      return render(request, 'signup.html')
    except Exception as e:
      messages.error(request,f"Error: {str(e)}")
      return render (request,"signup.html")
  else:
    return render (request,'signup.html')

def dashboardbloglist(request):
  user = request.user
  blogs = Blog.objects.filter(authorid=user).order_by('-publishdate')
  template = loader.get_template('dashboardblog.html')
  context = {
    'blogs': blogs,
  }
  return HttpResponse(template.render(context, request))

def addblogpageloader(request):
    if request.user.is_anonymous:
        return redirect("/login")

    if request.user.is_superuser:
        context = {'categories': Category.objects.all()}
        
        if request.method == 'POST':
            try:
                blogtitle = request.POST.get('blogtitle')
                blogcontent = request.POST.get('content')
                category_id = request.POST.get('category')
                featureimage = request.POST.get('featuredimage')
                authorid = request.user.id

                # Validate the inputs
                if not blogtitle or not blogcontent or not category_id or not featureimage:
                    messages.error(request, "All fields are required.")
                    return render(request, 'addblog.html', context)

                category = Category.objects.get(id=category_id)

                blog, created = Blog.objects.get_or_create(
                    category=category,
                    title=blogtitle,
                    content=blogcontent,
                    featuredimage=featureimage,
                    authorid=authorid
                )

                if created:
                    messages.success(request, "Your Blog Has Been Successfully Added!")
                else:
                    messages.warning(request, "A blog with this title already exists.")

            except Category.DoesNotExist:
                messages.error(request, "Selected category does not exist.")
            except Exception as e:
                messages.error(request, str(e))

        return render(request, 'addblog.html', context)
    
    messages.error(request, 'Access Denied')
    return redirect('/')