from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import connection
from .models import UserProfile
# Create your views here.

def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confPassword']
        profile_picture = request.FILES.get('profile_picture')  # Correct way to get uploaded file

        form_data = {
            'username': username,
            'email': email,
        }

        # Validations
        if not all([username, email, password, confirm_password]):
            messages.error(request, 'All fields are required.')
            return render(request, 'UserAuth/signup.html', context=form_data)

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'UserAuth/signup.html', context=form_data)

        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return render(request, 'UserAuth/signup.html', context=form_data)

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'UserAuth/signup.html', context=form_data)

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'UserAuth/signup.html', context=form_data)

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Create UserProfile with profile picture
        user_profile = UserProfile(user=user, profile_picture=profile_picture)
        user_profile.save()

        messages.success(request, 'Your account has been created successfully.')
        return redirect('user_login')

    return render(request, 'UserAuth/signup.html')

def user_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if username == '' or password == '':
            messages.error(request, 'All fields are required.')
            return render(request, 'UserAuth/login.html')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in.')

            if 'next' in request.GET:
                return redirect(request.GET['next'])
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid credentials.')

    return render(request, 'UserAuth/login.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('user_login')

@login_required
def update_user(request):
    user = request.user  
    user_profile, created = UserProfile.objects.get_or_create(user=user)  
    if request.method == 'POST':
        username = request.POST.get('username', user.username)
        email = request.POST.get('email', user.email)
        password = request.POST.get('password')
        confirm_password = request.POST.get('confPassword')
        profile_picture = request.FILES.get('profile_picture')
        if User.objects.exclude(id=user.id).filter(email=email).exists():
            messages.error(request, 'This email is already in use.')
            return redirect('update_user')
        if User.objects.exclude(id=user.id).filter(username=username).exists():
            messages.error(request, 'This username is already taken.')
            return redirect('update_user')
        if password:
            if len(password) < 6:
                messages.error(request, 'Password must be at least 6 characters long.')
                return redirect('update_user')
            if password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return redirect('update_user')
            user.set_password(password)
        user.username = username
        user.email = email
        user.save()

      
        if profile_picture:
            user_profile.profile_picture = profile_picture
            user_profile.save()

        messages.success(request, 'Your profile has been updated successfully.')
        return redirect('profile')
    return render(request, 'UserAuth/update_profile.html', {'user': user, 'profile': user_profile})