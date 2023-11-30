from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm, UpdateAnimeForm, UpdateMALUsernameForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from django.urls import reverse
from anime.models import Anime
from django.db.utils import DataError
import requests
import unicodedata
from django.urls.exceptions import NoReverseMatch


def register(request):
    if request.user.is_authenticated:
        return redirect('common-anime-chat-home')  # Redirect to the home page if the user is already logged in
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')  # Redirect to the home page after successful registration
        else:
            # If the form is not valid, re-render the registration page with the form containing validation errors
            return render(request, 'users/register.html', {'form': form})
    else:
        form = UserRegistrationForm()
        return render(request, 'users/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('common-anime-chat-home')
        return super().dispatch(request, *args, **kwargs)
    
@login_required
def profile(request):
    user = request.user
    context = {
        'user':user
    }

    return render(request, 'users/profile.html',context=context)

@login_required
def update_profile(request):
    user = request.user
    if request.method == "POST":
        print("INSIDE POST CONDITIONAL")
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=user.profile)
        anime_form = UpdateAnimeForm(request.POST)
        MAL_form = UpdateMALUsernameForm(request.POST)
        profile_owner = Profile.objects.get(pk=user.id)
        if 'update_user_profile' in request.POST:
            print("INSIDE USER FORM CONDITIONAL")
            print('User form validity:',u_form.is_valid())
            print('Profile form validity:',p_form.is_valid())
            if u_form.is_valid() and p_form.is_valid():
                print("USER FORM IS VALID")
                u_form.save()
                p_form.save()
                messages.success(request, f'Your account has been updated.') 
                return redirect('profile')
            else:
                print("USER FORM ERRORS:", u_form.errors)
                print("PROFILE FORM ERRORS:", p_form.errors) 
        elif 'update_MAL_username' in request.POST and MAL_form.is_valid():
            MAL_username = MAL_form.cleaned_data['MAL_username']
            new_username = MAL_username
            try:
                redirect_url = reverse('link_MAL_account', args=[new_username])
            except NoReverseMatch:
                profile_owner.MyAnimeList_username = ''
                return redirect('update_profile')
            redirect_url += f'?redirected=true&username={new_username}'
            return redirect(redirect_url)
        elif 'update_anime' in request.POST and anime_form.is_valid():
            normalized_anime = unicodedata.normalize('NFKD', anime_form.cleaned_data['watched_anime_list']).encode('ascii', 'ignore').decode('utf-8')
            anime_list = normalized_anime.split('\r\n')
            profile_owner.watched_anime.clear()
            for anime_name in anime_list:
                try:
                    # Try to get the anime, and if it doesn't exist, create it
                    anime, created = Anime.objects.get_or_create(title=anime_name)
                    
                    # Check if the anime was created (not already in the database)
                    if created:
                        anime.save()
                        
                    # Check if the user already has this anime in their watched_anime
                    if anime not in profile_owner.watched_anime.all():
                        profile_owner.watched_anime.add(anime)
                        
                except DataError:
                    print('DataError:',DataError)
                    print(f'Data error caused by the anime: {anime_name}')
        messages.success(request, 'Your anime list has been updated successfully!')
        return redirect('update_profile')


    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=user.profile)
        profile_owner = Profile.objects.get(user_id=user.id)
        watched_anime_names = [anime.title for anime in profile_owner.watched_anime.all()]
        watched_anime_list = '\n'.join(watched_anime_names)
        initial_anime_data = {'watched_anime_list': watched_anime_list}
        initial_MAL_username = {'MAL_username':profile_owner.MyAnimeList_username}
        anime_form = UpdateAnimeForm(initial=initial_anime_data)
        MAL_form = UpdateMALUsernameForm(initial=initial_MAL_username)

    context = {
        'u_form':u_form,
        'p_form':p_form,
        'anime_form':anime_form,
        'MAL_form':MAL_form,
        'user':user
    }

    return render(request, 'users/update_profile.html',context=context)

# class ViewProfileView(DetailView):
#     model = User
#     template_name = 'users/view_profile.html'
#     context_object_name = 'user'
def view_profile(request, user_id):
    profile_owner = User.objects.get(pk=user_id)
    viewer = request.user
    context = {
        'profile_owner':profile_owner,
        'viewer':viewer
    }

    return render(request, 'users/view_profile.html',context=context)

def link_MAL_account(request, username):
    redirected = request.GET.get('redirected')
    
    if redirected == 'true':
        username = request.GET.get('username')
        print('Username inside link function:', username)
        profile_owner = Profile.objects.get(user_id=request.user.id)
        profile_owner.watched_anime.clear()

        # Update the MAL username in the user's profile
        profile_owner.MyAnimeList_username = username
        profile_owner.save()

        page1 = f"https://api.myanimelist.net/v2/users/{username}/animelist"
        L1 = []
        
        while True:
            try:
                url = page1
                r = requests.get(url, headers={'X-MAL-CLIENT-ID':'4293c28cdc0ceac6c00919e569062f4b'})
                dictionary = r.json()
                
                for i in dictionary['data']:
                    L1.append(i['node']['title'])
                
                page1 = dictionary['paging']['next']
                
            except:
                break
        
        for anime_name in L1:
            try:
                # Try to get the anime, and if it doesn't exist, create it
                anime, created = Anime.objects.get_or_create(title=anime_name)
                
                # Check if the anime was created (not already in the database)
                if created:
                    anime.save()
                    
                # Check if the user already has this anime in their watched_anime
                if anime not in profile_owner.watched_anime.all():
                    profile_owner.watched_anime.add(anime)
                    
            except DataError:
                print('DataError:',DataError)
                print(f'Data error caused by the anime: {anime_name}')
     
        messages.success(request, 'Your MAL account has been linked successfully!')
        return redirect('update_profile')
    
    else:
        return redirect('common-anime-chat-home')

