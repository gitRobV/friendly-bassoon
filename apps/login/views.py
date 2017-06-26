# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.db.models import Count
from .models import User, Secret

# Index Get Route
def index(request):
    # If user status not set in Session redirect to login.
    if 'user_status' not in request.session or request.session['user_status'] != 'Authenticated':
        return redirect('/login')
    # Else get User for user_id in session
    else:
        user = User.objects.get(id=request.session['user_id'])
        secrets = Secret.objects.all()
        recent_secrets = secrets.order_by('-created_at')[:5]
        popular_secrets = secrets.annotate(num=Count('user_likes')).order_by('-num')[:5]
        user_likes = Secret.objects.filter(user_likes__id = user.id)

    # Render index.html
    return render(request, 'login/index.html', {'user': user, 'recent_secrets': recent_secrets, 'user_likes': user_likes, 'popular_secrets': popular_secrets})

# Login Get Route
def login(request):
    return render(request, 'login/login.html')

# Process Login Post Authentication
def authenticate(request):
    # Verify Request is of type POST
    if request.method == 'POST':
        # Copy Post Data
        post_data = request.POST.copy()
        # Pass Post Data copy int UserManager check_login
        validated = User.objects.check_login(post_data)
        # Check if any errors during Validation
        if len(validated.errors) > 0:
            # If Errors - loop through error messages and populate to messages
            messages.error(request, "Hol'up, Try that shit again.")
            for err in validated.error:
                messages.error(request, err)
            # Redirect to Index route
            return redirect('/')
        else:
        # If Validation had 0 errors
             # Set Session with user info
            request.session['user_id'] = validated.data['id']
            request.session['user_status'] = validated.data['status']
            # populate success message
            messages.success(request, "Welcome Back!")
    # redirect to index route
    return redirect('/')

# Register Get Route
def register(request):
    return render(request, 'login/register.html')

# Process Post Request from Register
def process(request):
    if request.method == 'POST':
        validated = User.objects.check_register(request.POST)
        if len(validated.errors) == 0:
            try:
                check_user = User.objects.get(email=validated.data['email'])
            except:
                check_user = False
            if check_user:
                data = {
                'f_name' :request.POST['f_name'],
                'l_name': request.POST['l_name'],
                'email': request.POST['email']
                }
                request.session['data'] = data
                messages.error(request, 'The Email provided is already registered. Choose a different email or login.')
                return redirect('/register')
            else:
                new_user = User.objects.create(f_name=validated.data['f_name'], l_name=validated.data['l_name'], email=validated.data['email'], password=validated.data['password'])
                request.session['user_id'] = new_user.id
                request.session['user_status'] = 'Authenticated'
                messages.success(request, 'Thank You for registering! Your user_id is ' + str(new_user.id))
                if 'data' in request.session:
                    del request.session['data']
                return redirect('/')
        else:
            for err in validated.errors:
                messages.error(request, err)
            return redirect('/register')

    return redirect('/register')

# Logout Flushes Session data
def logout(request):
    request.session.flush()
    return redirect('/')

def post_secret(request):
    if request.method == 'POST':
        request.session['process'] = 'Secret is being processed'
        post_data = request.POST.copy()
        submitted_secret = Secret.objects.create_secret(post_data)
        request.session['submitted_secret'] = submitted_secret
    return redirect('/')

def like_secret(request, secret_id):
    user = User.objects.get(id=request.session['user_id'])
    liked_secret = Secret.objects.get(id=secret_id)
    liked_secret.user_likes.add(user)

    return redirect('/')

def unlike_secret(request, secret_id):
    user = User.objects.get(id=request.session['user_id'])
    unliked_secret = Secret.objects.get(id=secret_id)
    unliked_secret.user_likes.remove(user)

    return redirect('/')

def delete_secret(request, secret_id):
    secret = Secret.objects.get(id=secret_id)
    secret.delete()
    return redirect('/')
