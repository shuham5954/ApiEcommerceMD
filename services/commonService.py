import httpx
from fastapi import HTTPException
import os
from dotenv import load_dotenv
import requests

load_dotenv()

KEYCLOAK_BASE_URL = os.getenv("KEYCLOAK_URL")  
KEYCLOAK_REALM = os.getenv("REALM")            
CLIENT_ID = os.getenv("CLIENT_ID")             
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

async def get_access_token():

    url = f"{KEYCLOAK_BASE_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        # "username":"test2",
        # "password":"123123"
    }
    response = requests.post(url, data=data)

    if response.status_code == 200:
      token_info = response.json()
      access_token = token_info.get("access_token")
      return access_token

    else:
      print("Error:", response.status_code, response.text)

async def get_refresh_token(ref_token):
  url = f"{KEYCLOAK_BASE_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
  data = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": ref_token,
    }
  response = requests.post(url, data=data)
 

  if response.status_code == 200:
      token_info = response.json()
      access_token = token_info
      return access_token

  else:
      print("Error:", response.status_code, response.text)


async def createUser(data):
  token = await get_access_token()
  hea = {
         "authorization":f"Bearer {token}",
         "Content-Type": "application/json"
        }
  url=f"{KEYCLOAK_BASE_URL}/admin/realms/{KEYCLOAK_REALM}/users"
  payload={
          "username": data.username,
          "email": data.email,
          "enabled": True,
          "attributes": {
          "mobile_number": data.phoneNumber  
                        },
          "credentials": [{
            "type": "password",
           "value": data.password,
           "temporary": False 
                          }]
  }
  async with httpx.AsyncClient() as client:
    response = await client.post(url,json=payload,headers=hea)
    if response.status_code == 201:
      return {"message": "User created successfully"}
    else:
      raise HTTPException(status_code=response.status_code, detail=response.json())