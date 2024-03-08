import requests
from requests.auth import HTTPBasicAuth
import json
import os
from dotenv import load_dotenv

load_dotenv()


client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_url = 'https://localhost:8888/callback'

scopes = "user-top-read"


def get_token(redirect_url, access_code=0, grantType='authorization_code'):
    url = 'https://accounts.spotify.com/api/token'
    basicAuth = HTTPBasicAuth(username=client_id,password=client_secret)
    header = {"content-type": "application/x-www-form-urlencoded"}

    if access_code==0:
        data = { 'grant_type': grantType}
        response = requests.post(url, params=data,headers=header, auth=basicAuth)

        if response.status_code == 200:
            token_data = response.json()
            # print(token_data)
            access_token = token_data['access_token']
            print("Access Token:", access_token)
            return access_token
        else:
            print("Failed to retrieve access token:", response.text)

    else:
        data = {
            'grant_type': grantType,
            'redirect_uri': redirect_url,
            'code': access_code
            }
        response = requests.post(url, params=data,headers=header, auth=basicAuth)

        if response.status_code == 200:
            token_data = response.content
            # print(token_data)
            access_token = token_data['access_token']
            print("Access Token:", access_token)
            return access_token
        else:
            print("Failed to retrieve access token:", response.text)


def search(query: str):

    access_token = get_token(redirect_url, grantType="client_credentials")

    if access_token:
        url = "https://api.spotify.com/v1/search"
        header = {'Authorization' : f'Bearer {access_token}'}
        params = {
            "q": query,
            "type": "artist",
            "limit": 3
        }


        response = requests.get(url=url, headers=header, params=params)
        if response.status_code == 200:
            # print(response.json())
            # return response.json()
            return json.loads(response.text)
        else:
            print(response.status_code)
            print(response.json())
            return response.status_code
    else:
        raise AttributeError('No Token Provided')
        print("No access token received. Need access token to use search.")
    
if __name__ == "__main__":
    response = search("Lindsey Stirling")
    print(response)