# views.py
import requests
import datetime
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect

import logging
from django.views import View

import sys

from django.views.decorators.csrf import csrf_exempt
from requests import Response
from rest_framework.views import APIView

from accounts.models import SallaOAuthData

MY_DOMAIN = 'http://127.0.0.1:8000/'
CLIENT_ID = '4e873f29-deff-49f9-a9e8-53f25a5be946'
CLIENT_SECRET = '47f5ace49f73e490de4e55febda6b768'

LOG_FORMAT = "%(asctime)s  %(filename)s: %(funcName)s" \
             " line: %(lineno)-3d %(levelname)s  %(message)s "
formatter = logging.Formatter(LOG_FORMAT)
# pylint: disable=C0209
today_log = 'log_{:%m_%d_%Y}.log'.format(datetime.datetime.now())
file_handler = logging.FileHandler(today_log)
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)


class SallaOAuthView(View):
    logging.warning(f'### START SallaOAuthView ###')

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        logging.warning(f'START SallaOAuthView : {request.GET}')

        if 'code' not in request.GET:
            logging.info(f'CODE: {request.GET}')
            # Redirect the user to Salla's authorization URL
            salla_auth_url = "https://accounts.salla.sa/oauth2/auth"
            client_id = CLIENT_ID  # Replace with your actual client ID
            redirect_uri = f"{MY_DOMAIN}salla/oauth/callback/"  # Update with your actual callback URL
            auth_url = f"{salla_auth_url}?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=offline_access"
            return JsonResponse({'auth_url':auth_url})

        authorization_code = request.GET.get('code')
        salla_token_url = "https://accounts.salla.sa/oauth2/token"
        client_id = CLIENT_ID  # Replace with your actual client ID
        client_secret = CLIENT_SECRET  # Replace with your actual client secret
        redirect_uri = f"{MY_DOMAIN}salla/oauth/callback/"  # Update with your actual callback URL

        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri": redirect_uri,
        }

        response = requests.post(salla_token_url, data=data)
        token_data = response.json()

        # Store the access token and refresh token in your database
        access_token = token_data['access_token']
        refresh_token = token_data['refresh_token']

        # Use the access token to fetch merchant details
        salla_user_url = "https://accounts.salla.sa/oauth2/user/info"
        headers = {"Authorization": f"Bearer {access_token}"}
        user_response = requests.get(salla_user_url, headers=headers)
        user_data = user_response.json()

        # Now you can use user_data to access merchant details
        # and perform further actions as needed

        return redirect(f"{MY_DOMAIN}/success/")


class SallaOAuthCallbackView(View):
    logging.warning(f"### START SallaOAuthCallbackView ### ")
    @csrf_exempt
    def get(self, request, *args, **kwargs):
        if 'code' in request.GET:
            logging.warning(f"GET METHOD {request.GET} ")
            print(request)
            code = request.GET['code']
            salla_token_url = "https://accounts.salla.sa/oauth2/token"
            client_id = CLIENT_ID  # Replace with your actual client ID
            client_secret = CLIENT_SECRET  # Replace with your actual client secret
            redirect_uri = f"{MY_DOMAIN}salla/oauth/callback/"  # Update with your actual callback URL

            data = {
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect_uri,
            }
            logging.warning(f"DATA{data}")
            response = requests.post(salla_token_url, data=data)
            token_data = response.json()

            # Store the access token and refresh token in your database
            access_token = token_data['access_token']
            refresh_token = token_data['refresh_token']
            logging.warning(f"{access_token}/n{refresh_token}")
            # Use the access token to fetch merchant details
            salla_user_url = "https://accounts.salla.sa/oauth2/user/info"
            headers = {"Authorization": f"Bearer {access_token}"}
            user_response = requests.get(salla_user_url, headers=headers)
            user_data = user_response.json()

            # Now you can use user_data to access merchant details
            # and perform further actions as needed

            return redirect(f"{MY_DOMAIN}salla/oauth/success/")  # Redirect to a success page
        else:
            return redirect(f"{MY_DOMAIN}salla/oauth/error/")


class SallaOAuthSuccessView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"message": "OAuth authentication successful"})


class SallaOAuthErrorView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"error": "OAuth authentication failed"})


from django.shortcuts import redirect
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

# Salla OAuth 2.0 configuration
client_id = CLIENT_ID
client_secret = CLIENT_SECRET
REDIRECT_URI = f'{MY_DOMAIN}new/salla/oauth/callback/'
# authorization_base_url = 'https://accounts.salla.sa/oauth2/authorize'
authorization_base_url = 'https://accounts.salla.sa/oauth2/auth'
token_url = 'https://accounts.salla.sa/oauth2/token'


class SallaAuthorizationView(APIView):
    def get(self, request):
        salla = OAuth2Session(client_id, redirect_uri=REDIRECT_URI, scope=['offline_access'])
        authorization_url, state = salla.authorization_url(authorization_base_url)

        return JsonResponse({'authorization_url':authorization_url,
                             'state':state})


class SallaCallbackView(APIView):
    def get(self, request):
        salla = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
        token = salla.fetch_token(
            token_url,
            authorization_response=request.build_absolute_uri(),
            client_secret=client_secret,
        )

        # Extract data
        access_token = token['access_token']
        refresh_token = token.get('refresh_token')
        expires_at = datetime.utcfromtimestamp(token['expires_at'])
        user_info = salla.get('https://accounts.salla.sa/oauth2/user/info').json()
        api_response = salla.get('https://api.salla.dev/admin/v2/orders').json()

        # Save data to the model
        oauth_data = SallaOAuthData.objects.create(
            user_info=user_info,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at,
            api_response=api_response
        )

        logging.warning(f"Data saved to model: {oauth_data}")

        return Response("OAuth 2.0 process completed.")