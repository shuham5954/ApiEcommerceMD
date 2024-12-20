import httpx
from fastapi import HTTPException
import os
from dotenv import load_dotenv
import requests
from models.account import user_log_in , UserCreate

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
         "Authorization":f"Bearer {token}",
         "Content-Type": "application/json"
        }
  url=f"{KEYCLOAK_BASE_URL}/admin/realms/{KEYCLOAK_REALM}/users"
  payload={
          "username": data.user_name,
          "email": data.email,
          "enabled": True,
          "attributes": {
          "mobile_number": data.phone_number  
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
      user_id = await get_user_info(data.user_name)
      print(user_id)
      await assign_role(user_id)
      return {"message": "User created successfully"}
    else:
      raise HTTPException(status_code=response.status_code, detail=response.json())

# for getting user info 
async def get_user_info(user_name:str):
  token = await get_access_token()
  hea = {
         "authorization":f"Bearer {token}",
         "Content-Type": "application/json"
        }
  url = f"{KEYCLOAK_BASE_URL}/admin/realms/{KEYCLOAK_REALM}/users?username={user_name}"
  async with httpx.AsyncClient() as client:
    response = await client.get(url,headers=hea)
    if response.status_code == 200 or response.status_code == 204:
      user_id = response.json()[0]['id']
      return user_id
    else:
      raise HTTPException(status_code=response.status_code, detail=response.json())
  

async def assign_role(user_id:str):
  id = user_id
  print(id)
  token = await get_access_token()
  hea = {
         "Authorization":f"Bearer {token}",
         "Content-Type": "application/json"
        }
  url = f"{KEYCLOAK_BASE_URL}/admin/realms/{KEYCLOAK_REALM}/users/{id}/role-mappings/realm"
    # http://localhost:8080/auth/admin/realms/{your-realm}/users/{user-id}/role-mappings/realm
  payload=[{
        "id": "ffa143a8-a5e6-4f48-918b-9f2663804ee4",
        "name": "user"
        }]
  async with httpx.AsyncClient() as client:
    response = await client.post(url,json=payload,headers=hea)
    if response.status_code == 204:
      return response.status_code
    else:
      raise HTTPException(status_code=response.status_code, detail=response.json())
    
  # return True

async def user_token(data:user_log_in):
  url = f"{KEYCLOAK_BASE_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
  payload = {
      "grant_type": "password",
      "client_id": CLIENT_ID,
      "client_secret": CLIENT_SECRET,
      "username":data.user_name,
      "password":data.password
    
   }
  async with httpx.AsyncClient() as client:
    response = await client.post(url , data= payload )
    if response.status_code == 200:
      return response.json()
    else:
      print("Error:", response.status_code, response.text)

      
  



