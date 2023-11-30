from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from users.models import Profile
from .models import ChatRoom
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django.urls import reverse
import requests
import random
from django.http import JsonResponse
import json
import string
# import unicodedata

def generate_random_string(length=32):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


def match_anime_list(username1, username2):
    """Checks if two users have watched the same anime and if they have, returns a list of the common anime they have watched."""
    user_1 = User.objects.get(username=username1)
    user_2 = User.objects.get(username=username2)
    profile_1 = Profile.objects.get(user_id=user_1.id)
    profile_2 = Profile.objects.get(user_id=user_2.id)
    user_1_anime_list = profile_1.watched_anime.all()
    user_2_anime_list = profile_2.watched_anime.all()
    # CAP_1 = [anime_name.capitalize() for anime_name in user_1_anime_list]
    # CAP_2 = [anime_name.capitalize() for anime_name in user_2_anime_list]
    match_found = False
    common_anime = []
    for anime in user_1_anime_list:
        if anime in user_2_anime_list:
            common_anime.append(anime)
            match_found = True
    if match_found == True:
        return common_anime
    else:
        return None
    
def start_chat(request):
    if request.user.is_authenticated:
        if request.user.profile.MyAnimeList_username != None or request.user.profile.watched_anime.all() != None:
            # Get the current user's MyAnimeList username
            # current_user_mal_username = request.user.profile.MyAnimeList_username

                # Get all other active users
            # active_users = Profile.objects.filter(is_active=True).exclude(user=request.user)
            # profiles = Profile.objects.all()
            # Users = User.objects.all()
                # Create a dictionary to store potential chat partners
            potential_chat_partners = {}
            # user_chats = ChatRoom.objects.filter(particicpants=request.user.profile)

            # for user in Users:
            #     try:
            #         user_profile = Profile.objects.get(user_id=user.id)
            #     except Profile.DoesNotExist:
            #         continue
            #     for chatroom in user_chats:
            #         if user_profile not in chatroom.participants.all():
            #     # print(f"{user_profile.id}'s MAL username: {user_profile.MyAnimeList_username}")
            #             if user_profile.MyAnimeList_username != request.user.profile.MyAnimeList_username:
            #                 if len(user_profile.watched_anime.all()) != 0:
            #                     # print("MAL username inside if statement: "+user_profile.MyAnimeList_username)
            #                     common_anime = match_anime_list(request.user.username, user.username)
            #                     if common_anime:
            #                         print("COMMON ANIME FOUND.")
            #                             # If there is at least one common anime, add the user_profile to potential chat partners
            #                         potential_chat_partners[user] = common_anime
            #                     else:
            #                         continue
            #                 else:
            #                     continue
            #             else:
            #                 continue
            #         else:
            #             break   
            user_chats = ChatRoom.objects.filter(participants=request.user.profile)

            # Initialize a dictionary to store potential chat partners
            potential_chat_partners = {}

            # Get all users
            all_users = User.objects.all()

            for user in all_users:
                # Skip the current user
                if user == request.user:
                    continue
                
                try:
                    user_profile = Profile.objects.get(user=user)
                except Profile.DoesNotExist:
                    continue

                # Check if the user_profile is not part of any of the user_chats
                if not any(user_profile in chatroom.participants.all() for chatroom in user_chats):
                    # Check other conditions for potential chat partners
                    if (
                        user_profile.MyAnimeList_username != request.user.profile.MyAnimeList_username
                        and len(user_profile.watched_anime.all()) > 0
                    ):
                        common_anime = match_anime_list(request.user.username, user.username)
                        if common_anime:
                            # Store the user and associated data in the dictionary
                            potential_chat_partners[user] = common_anime     
            if potential_chat_partners:
                    # If there are potential chat partners, pick a random one
                potential_partners = list(potential_chat_partners.keys())
                random_partner = random.choice(potential_partners)
                # random_partner = Profile.objects.get(partner_random.id)
                chatroom_name = generate_random_string()
                chatroom = ChatRoom.objects.create(name=chatroom_name)
                chatroom.participants.add(request.user.profile, random_partner.profile)
                partner_common_anime = potential_chat_partners[random_partner]
                # common_anime_partner = ', '.join(partner_common_anime)
                common_anime_partner = []
                
                
                for anime in partner_common_anime:
                    common_anime_partner.append(anime.title)
                s = str(common_anime_partner)
                new_s = s[1:-1]
                result_string = new_s.replace("'",'')
                # normalized_string = unicodedata.normalize('NFKD', result_string).encode('ascii', 'ignore').decode('utf-8')
                messages.success(request, f'({random_partner.username})Both of you have watched {result_string}!')
                return redirect('room', room_name=chatroom_name)
            else:
                messages.success(request, f'No user who has watched the same anime as you was found, try again later :(')
                return redirect('common-anime-chat-home')

                # If no potential chat partner found, show a message or handle the case as you wish
        else:
            messages.success(request, 'You need to add your MyAnimeList username or add the anime you have watched in your profile.')
            return redirect('update_profile')


        return redirect('common-anime-chat-home')  # Redirect to the index page if no chat partner found
    else:
        messages.success(request, f'You need to log in to chat.')
        return redirect('login')

def home(request):
    context = {
        }
    return render(request, 'common_anime_chat/index.html', context)


def about(request):
    return render(request, 'common_anime_chat/about.html')


def room(request, room_name):
    if request.user.is_authenticated:
        print(room_name)
        try:
            print('room name:', room_name)
            chatroom = ChatRoom.objects.get(name=room_name)
        except ChatRoom.DoesNotExist:
            messages.success(request, f'Chatroom not found.')
            return redirect('common-anime-chat-home')

        if request.user.profile not in chatroom.participants.all():
            messages.success(request, f'You are not a participant in this chat.')
            return redirect('common-anime-chat-home')
        
        for user_profile in chatroom.participants.all():
            if request.user.profile != user_profile:
                chat_partner = user_profile

        return render(request, 'common_anime_chat/chatroom.html', {
            'room_name': room_name,
            'chat_partner':chat_partner,
        })
    else:
        messages.success(request, f'You need to log in to start conversations.')
        return redirect('login')


def get_user_profile_pictures(request):
    # Get all users
    profiles = Profile.objects.all()

    # Create a dictionary to store the profile picture URLs for each user
    profile_pictures = {}
    for profile in profiles:
        # Check if the user has a profile picture
        profile_pictures[profile.user_id] = profile.profile_picture.url

    return JsonResponse(profile_pictures)

def update_active_status(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'Fetch':
        data = json.loads(request.body.decode('utf-8'))
        user_id = data.get('user_id')
        is_active = data.get('is_active')
        if user_id is not None and is_active in [True, False]:
            profile = Profile.objects.filter(user_id=user_id).first()
            if profile:
                profile.set_active_status(is_active)
                return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

def user_chat(request):
    # print("User id:", User.objects.get(pk=user_id).username)
    profile_owner = Profile.objects.get(user_id=request.user.id)
    user_chatrooms = ChatRoom.objects.filter(participants=profile_owner)
    participants_besides_user = []
    profiles_besides_user = []
    for chatroom in user_chatrooms:
        for participant in chatroom.participants.all():
            if participant.user_id == request.user.id:
                continue
            else:
                participant_user = User.objects.get(pk=participant.user_id)
                participants_besides_user.append(participant_user)
                profiles_besides_user.append(participant)

    context = {
        'user_chatrooms':user_chatrooms,
        'chat_participants':participants_besides_user,

    }

    return render(request, 'common_anime_chat/user_chats.html', context)

def start_chat_button(request, username):
    if request.user.is_authenticated:
        second_user = User.objects.get(username=username)
        second_profile = Profile.objects.get(user_id=second_user.id)
        second_user_chats = ChatRoom.objects.filter(participants=second_profile)
        for chatroom in second_user_chats:
            if request.user.profile in chatroom.participants.all():
                return redirect('room', room_name=chatroom.name)
        chatroom_name = generate_random_string()
        chatroom = ChatRoom.objects.create(name=chatroom_name)
        chatroom.participants.add(request.user.profile, second_user.profile)
        return redirect('room', room_name=chatroom_name)
    else:
        messages.success(request, f'You need to log in before starting a chat.')
        return redirect('login')

def search_users(request):
    if request.method == 'GET':
        search_query = request.GET.get('search_query', '')
        print('Search query:',search_query)

        # Query the Users table for users with usernames containing the search query
        users = User.objects.filter(username__icontains=search_query)

        context = {
            'users': users,
            'search_query': search_query,
        }

        return render(request, 'common_anime_chat/search_results.html', context)

def get_urls(request):
    try:  
        if request.method == "GET":
            urls = {
                'home':reverse('common-anime-chat-home'),
                'profile':reverse('profile'),
                'login':reverse('login'),
                'logout':reverse('logout'),
                'register':reverse('register'),
                'about_us':reverse('common-anime-chat-about'),
                'my_chats':reverse('user_chat'),

            }
            return JsonResponse(urls)
    except Exception as e:
        print('Error:',e)
        return JsonResponse({'error': str(e)}, status=500)