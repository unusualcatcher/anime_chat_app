from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='common-anime-chat-home'),
    path('about/', views.about, name='common-anime-chat-about'),
    path('chat/<str:room_name>/', views.room, name='room'),
    path('api/get_user_profile_pictures/', views.get_user_profile_pictures, name='get_user_profile_pictures'),
    path('start-chat/', views.start_chat, name='start_chat'),
    path('update_active_status/', views.update_active_status, name='update_active_status'),
    path('chats/', views.user_chat, name='user_chat'),
    path('start-conversation/<str:username>', views.start_chat_button, name='chat_start'),
    path('search-users', views.search_users, name='search_users'),
    path('get_urls/', views.get_urls, name='get_urls')

]
