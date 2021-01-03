from .models import SpotifyToken
from django.utils import timezone
from datetime import timedelta
from requests import post,put,get

import os
from dotenv import load_dotenv
load_dotenv()

#Create the .env file including CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
#CLIENT_ID and CLIENT_SECRET are obtained from Spotify Developer Dashboard
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

BASE_URL = "https://api.spotify.com/v1/me/"

def get_user_tokens(session_id):
    user_tokens = SpotifyToken.objects.filter(user=session_id)
    if user_tokens.exists():
        return user_tokens.first()
    return None


def update_or_create_user_tokens(session_id,access_token,token_type,expires_in,refresh_token):
    tokens = get_user_tokens(session_id)
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token','refresh_token','expires_in','token_type'])
    else:
        tokens = SpotifyToken.objects.create(
            user=session_id,
            access_token=access_token,
            refresh_token=refresh_token,
            token_type=token_type,
            expires_in=expires_in
        )
    


def is_spotify_authenticated(session_id):
    tokens = get_user_tokens(session_id)
    if tokens:
        expiry = tokens.expires_in
        if expiry <= timezone.now():
            refresh_spotify_token(session_id,tokens)
        return True
    return False


def refresh_spotify_token(session_id,tokens):
    refresh_token = tokens.refresh_token

    response = post("https://accounts.spotify.com/api/token",data={
        'grant_type':'refresh_token',
        'refresh_token':refresh_token,
        'client_id':CLIENT_ID,
        'client_secret':CLIENT_SECRET,
    }).json()

    access_token = response.get("access_token")
    token_type = response.get("token_type")
    expires_in = response.get("expires_in")

    update_or_create_user_tokens(session_id,access_token,token_type,expires_in,refresh_token)



def execute_spotify_api_request(session_id,endpoint,post_=False,put_=False):
    tokens = get_user_tokens(session_id)
    headers = {"Content-Type":'application/json','Authorization':"Bearer "+ tokens.access_token}
    if post_:
        post(BASE_URL + endpoint, headers=headers)
    if put_:
        r = put(BASE_URL + endpoint, headers=headers)
        print(r)
    
    response = get(BASE_URL+endpoint,{},headers=headers)

    try:
        return response.json()
    except:
        return {"Error":"Issue with Request!"}


def play_song(session_id):
    return execute_spotify_api_request(session_id,"player/play",put_=True)


def pause_song(session_id):
    return execute_spotify_api_request(session_id,"player/pause",put_=True)
