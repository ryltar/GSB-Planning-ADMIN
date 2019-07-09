from flask import Flask, request
import requests
import json

class Authentification:

   def postAuth(self,pseudo,password):
      payload = {'email':pseudo, 'passwd':password}
      url = "http://claudioppe.ddns.net/auth/token"
      postAuth = requests.post(url, data=payload)
      return postAuth.json()