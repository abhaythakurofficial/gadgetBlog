from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Contact
from django.contrib import messages  # Import the messages module
from Blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout


def home(request):
    allposts = Post.objects.all()
    context={'allposts':allposts}
    return render(request, 'home/home.html',context)

def about(request):
    return render(request, 'home/about.html')

def writer(request):
    return render(request, 'home/writer.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        description = request.POST.get('description')

        if not name or not phone_number or not email or not description:
            messages.error(request, "Message: Please fill out all fields correctly.")
            return redirect('contact')
        else:
            contact = Contact(
                name=name,
                email=email,
                phone_number=phone_number,
                description=description
            )
            contact.save()
            messages.success(request, "Message: Your message has been sent successfully!")
            return redirect('contact')  # Redirect to avoid form resubmission

    return render(request, 'home/contact.html')

def search(request):
    search = request.GET.get('search')
    if len(search)>78:
        allposts=Post.objects.none()
    else:
        allpostsTitle=Post.objects.filter(title__icontains=search)
        allpostsContent=Post.objects.filter(content__icontains=search)
        allpostsAuthor=Post.objects.filter(author__icontains=search)
        allposts=allpostsTitle.union(allpostsContent,allpostsAuthor)
    if allposts.count()==0:
        messages.warning(request, "Message: Please refine search fields correctly.")
    context = {'allposts': allposts,'search':search}
    return render(request, 'home/search.html', context)

def handelSignup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')  # Should match the input name in the form
        lastname = request.POST.get('lastname')    # Should match the input name in the form
        email1 = request.POST.get('email1')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Check if passwords match
        if len(username) > 15:
            messages.error(request, "User name should be under 15 letter")
            return redirect('/')
        if not username.isalnum():
            messages.error(request, "User name should be letters and numbers")
            return redirect('/')
        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('/')

        # Create user here:
        myuser = User.objects.create_user(username=username, email=email1, password=password1)
        myuser.first_name = firstname  # Use firstname instead of fname
        myuser.last_name = lastname    # Use lastname instead of lname
        myuser.save()

        messages.success(request, 'Your gadgetBlog account has been created')
        return redirect('home')
    else:
        return HttpResponse('404 - This is not Found')

def handellogin(request):
    if request.method == 'POST':
        username1 = request.POST.get('username1')
        loginpassword = request.POST.get('loginpassword')
    
    user=authenticate(username=username1,password=loginpassword)
    
    if user is not None:
        login(request,user)
        messages.success(request, 'login is successfull')
        return redirect('home')
    else:
        messages.error(request, 'Invalid credentials, Please try again')
        return redirect('home')


    return HttpResponse('404 - page not found')

def handellogout(request):
    logout(request)
    messages.success(request, 'logout is successfull')
    return redirect('home')