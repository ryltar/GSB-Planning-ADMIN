from flask import Flask, request
from Address import * 
import requests
import json

class AddressService:

   def getAllAddress(self,token):
      url = "http://gsb-planning-api/admin/addresses"
      headers = {'authorization': token,
                  'Connection':'keep-alive'}
      allAddress = requests.get(url, headers=headers)
      return allAddress.json()

   def getOneAddress(self,token, id):
      url = "http://gsb-planning-api/admin/addresses/"+str(id)
      headers = {'authorization': token,
                  'Connection':'keep-alive'}
      OneAddress = requests.get(url, headers=headers)
      return OneAddress.json()


   def putOneAddress(self, token, address):
      url = "http://gsb-planning-api/admin/addresses/"+str(address.id)
      payload = address.dictionarize()
      del payload['id']
      headers = {'authorization': token,
                  'Content-Type': 'application/x-www-form-urlencoded'}
      putOneAddress = requests.put(url, headers=headers, data=payload)
      return putOneAddress

   def deleteOneAddress(self,token, key):
      url = "http://gsb-planning-api/admin/addresses/"+str(key)
      headers = {'authorization': token}
      deleteOneAddress = requests.delete(url, headers=headers)
      return deleteOneAddress

   def createOneAddress(self, token, address):
      url = "http://gsb-planning-api/admin/addresses"
      payload = address.dictionarize()
      del payload['id']
      headers = {'authorization': token,
                  'Content-Type': 'application/x-www-form-urlencoded'}
      postOneAddress = requests.post(url, headers=headers, data=payload)
      return postOneAddress