from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404
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
      messages.success(request, f'Hello {current_user}')
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
        
      user = User.objects.create_user(username,email,password,is_superuser=is_superuser, )
      user.first_name=fname
      user.last_name=lname
      user.email = email
      user.phone = phone
      user.is_staff = is_author
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
  if request.user.is_anonymous:
    return redirect('/login')
  else:
    user = request.user
    if request.user.is_superuser:
      blogs = Blog.objects.all().order_by('-publishdate')
    else:
      blogs = Blog.objects.filter(authorid=user).order_by('-publishdate')
    template = loader.get_template('dashboardblog.html')
    context = {
      'blogs': blogs,
    }
    return HttpResponse(template.render(context, request))

def addblogpageloader(request):
  if request.user.is_anonymous:
      return redirect("/login")

  if request.user.is_superuser or request.user.is_staff:
      context = {'categories': Category.objects.all()}
      
      if request.method == 'POST':
          try:
              blogtitle = request.POST.get('blogtitle')
              blogcontent = request.POST.get('content')
              category_name = request.POST.get('category')
              featuredimage = request.FILES.get('featuredimage')
              authorid = request.user

              # Validate the inputs
              if not blogtitle or not blogcontent or category_name == "choose" or not featuredimage:
                  messages.error(request, "All fields are required.")
                  return render(request, 'addblog.html', context)

              category = Category.objects.get(name=category_name)

              blog = Blog(
                  category=category,
                  title=blogtitle,
                  content=blogcontent,
                  featuredimage=featuredimage,
                  authorid=authorid
              )
              blog.save()

              messages.success(request, "Your Blog Has Been Successfully Added!")
              return redirect('/add-blog')  # Redirect to a blog list or success page after adding

          except Category.DoesNotExist:
              messages.error(request, "Selected category does not exist.")
          except Exception as e:
              messages.error(request, str(e))
      
      return render(request, 'addblog.html', context)
  
  messages.error(request, 'Access Denied')
  return redirect('/')


#still issue remaining
def editblogpageloader(request, id):
    if request.user.is_anonymous:
        return redirect('/login')
    
    blog = get_object_or_404(Blog, id=id)
    context = {
        'blog': blog,
        'categories': Category.objects.all()
    }
    
    if request.method == "POST":
        btitle = request.POST.get('blogtitle')
        bcat = request.POST.get('category')
        bcontent = request.POST.get('content')
        bimg = request.FILES.get('featuredimage')
        
        try:
            blog.title = btitle
            blog.content = bcontent
            
            if bimg:
                blog.featuredimage = bimg
            
            blog.category = get_object_or_404(Category)
            blog.save()
            
            messages.success(request, "Blog updated successfully!")
            return redirect('/edit-blog/' + str(id))
            
        except Exception as e:
            messages.error(request, f"Issue updating: {e}")
            return redirect('/edit-blog/' + str(id))
    
    return render(request, 'editblog.html', context)

def logout_view(request):
  logout(request)
  return redirect('home')

def dashboardcatlist(request):
  if request.user.is_anonymous:
    return redirect('/login')
  else:
    cat = Category.objects.all().order_by('name')
    template = loader.get_template('dash-cat-list.html')
    context = {
      'categories': cat,
    }
    return HttpResponse(template.render(context, request))
  
def addcatloader(request):
    if request.user.is_anonymous:
        return redirect("/login")
    
    if request.user.is_superuser or request.user.is_staff:        
        if request.method == 'POST':
            try:
                title = request.POST.get('categorytitle')
                content = request.POST.get('categorycontent')
                authorid = request.user

                # Validate the inputs
                if not title:
                    messages.error(request, "Title is required.")
                    return render(request, 'add-category.html')
                cat = Category(
                    name=title,
                    content=content,
                    author=authorid
                )
                cat.save()

                messages.success(request, "Your Category Has Been Successfully Added!")
                return redirect('/dashboard-addcat')  # Redirect to a blog list or success page after adding
            except Exception as e:
                messages.error(request, str(e))
        
        return render(request, 'add-category.html')
    
    messages.error(request, 'Access Denied')
    return redirect('/')

def deleteblogpage(request, id):
  if request.user.is_anonymous:
        return redirect('/login')
  try:
    delobj = Blog.objects.get(id=id)
    delobj.delete()
    messages.success(request, "Deletion Successful")
    return redirect('/dashboard-blog')
  except Exception as e:
    messages.error(request, "Deletion Unsuccessful")

def editcategorypage(request, id):
    if request.user.is_anonymous:
        return redirect('/login')
    
    category = Category.objects.get(id=id)

    context = {
        'cat': category
    }
    if request.user.is_superuser or request.user.is_staff:    
      if request.method == "POST":
          cattitle = request.POST.get('categorytitle')
          catcontent = request.POST.get('categorycontent')
          
          try:
              category.title = cattitle
              category.content = catcontent
              category.save()
              
              messages.success(request, "category updated successfully!")
              return redirect('/dashboard-editcat/' + str(id))
              
          except Exception as e:
              messages.error(request, f"Issue updating: {e}")
              return redirect('/dashboard-editcat/' + str(id))
      
      return render(request, 'edit-category.html', context)
    messages.error(request, 'Access Denied')
    return redirect('/')

def deletecategorypage(request, id):
  if request.user.is_anonymous:
        return redirect('/login')
  try:
    delobj = Category.objects.get(id=id)
    delobj.delete()
    messages.success(request, "Deletion Successful")
    return redirect('/dashboard-cat')
  except Exception as e:
    messages.error(request, "Deletion Unsuccessful")

def userlistpage(request):
  if request.user.is_anonymous:
    return redirect('/login')
  
  user = User.objects.all().order_by('first_name')
  template = loader.get_template('dashboard-userlist.html')
  context = {
    'users': user,
  }
  return HttpResponse(template.render(context, request))

def adduserpage(request):
  if request.user.is_anonymous:
    return redirect('/login')
  
  if not request.user.is_superuser:
    messages.error(request, 'Access Denied')
    return redirect('/')
  
  if request.method == 'POST':
    try:
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Validate the inputs
        if not firstname or not username or not email or not phone or not password:
            messages.error(request, "All fields are required.")
            return render(request, 'adduser.html')

        user = User(
            first_name=firstname,
            last_name=lastname,
            username=username,
            email=email,
            is_staff = True
        )
        user.set_password(password)  # Proper way to set password
        user.save()

        messages.success(request, "Your User Has Been Successfully Added!")
        return redirect('/dashboard-adduser')  # Redirect to a blog list or success page after adding

    except Exception as e:
        messages.error(request, str(e))
        return render(request, 'adduser.html')

  return render(request, 'adduser.html')  # Show the form if it's a GET request or if an error occurs