# chat/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'chat'

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('signup/', views.sign_up, name='sign_up'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('chat/', views.chat_interface, name='chat_interface'),
    path('messages/<int:user_id>/', views.get_messages, name='get_messages'),  # Route to fetch old messages
    path('messages/<int:user_id>/', views.chat_messages, name='chat_messages'),
    path('messages/<int:user_id>/', views.get_previous_messages, name='get_previous_messages'),  # Ensure this line is present
]
