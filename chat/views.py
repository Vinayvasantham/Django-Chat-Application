from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from .models import User, Message
from channels.db import database_sync_to_async
from .consumers import ChatConsumer


@login_required
@database_sync_to_async
def get_messages(request, user_id):
    current_user = request.user.username  # Validate session user
    messages = Message.objects.filter(sender=current_user, receiver_id=user_id) | \
               Message.objects.filter(sender_id=user_id, receiver=current_user)
    serialized_messages = [
        {"sender": msg.sender, "content": msg.content} for msg in messages
    ]
    return JsonResponse(serialized_messages, safe=False)

# Landing page view
def landing_page(request):
    if request.user.is_authenticated:
        return redirect('chat:chat_interface')
    return render(request, 'chat/landing.html')

# User signup view
def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('chat:login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'chat/signup.html', {'form': form})

# User login view
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Store user-specific session data
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            
            # Optional: Generate a unique session key for the user
            from uuid import uuid4
            request.session['session_key'] = str(uuid4())

            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('chat:chat_interface')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'chat/login.html', {'form': form})

# User logout view
def user_logout(request):
    logout(request)
    messages.info(request, "You have logged out successfully.")
    return redirect('chat:landing')

# Chat interface view
@login_required
def chat_interface(request):
    users = User.objects.all()
    return render(request, 'chat/chat_interface.html', {
        'users': users,
    })

def get_previous_messages(user_id):
    from .models import Message  # Import Message model here
    return list(Message.objects.filter(receiver_id=user_id).values('sender__username', 'content'))

async def chat_messages(request, user_id):
    messages = await ChatConsumer().get_previous_messages(user_id)
    return JsonResponse(messages, safe=False)
    
