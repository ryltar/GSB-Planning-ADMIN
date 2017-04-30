from flask import Flask, request
import requests
import json

class Authentification:

   def postAuth(self,pseudo,password):
      payload = {'email':pseudo, 'passwd':password}
      url = "http://gsb-planning-api/auth/token"
      postAuth = requests.post(url, data=payload)
      print(postAuth.json())
      return postAuth.json()