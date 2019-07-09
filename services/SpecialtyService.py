from flask import Flask, request
from Specialty import * 
import requests
import json

class SpecialtyService:

   def getAllSpecialty(self,token):
      url = "http://claudioppe.ddns.net/admin/specialties"
      headers = {'authorization': token,
                  'Connection':'keep-alive'}
      allSpecialty = requests.get(url, headers=headers)
      return allSpecialty.json()

   def getOneSpecialty(self,token, id):
      url = "http://claudioppe.ddns.net/admin/specialties/"+str(id)
      headers = {'authorization': token,
                  'Connection':'keep-alive'}
      OneSpecialty = requests.get(url, headers=headers)
      return OneSpecialty.json()


   def putOneSpecialty(self, token, specialty):
      url = "http://claudioppe.ddns.net/admin/specialties/"+str(specialty.id)
      payload = specialty.dictionarize()
      del payload['id']
      headers = {'authorization': token,
                  'Content-Type': 'application/x-www-form-urlencoded'}
      putOneSpecialty = requests.put(url, headers=headers, data=payload)
      return putOneSpecialty

   def deleteOneSpecialty(self,token, key):
      url = "http://claudioppe.ddns.net/admin/specialties/"+str(key)
      headers = {'authorization': token}
      deleteOneSpecialty = requests.delete(url, headers=headers)
      return deleteOneSpecialty

   def createOneSpecialty(self, token, specialty):
      url = "http://claudioppe.ddns.net/admin/specialties"
      payload = specialty.dictionarize()
      del payload['id']
      headers = {'authorization': token,
                  'Content-Type': 'application/x-www-form-urlencoded'}
      postOneSpecialty = requests.post(url, headers=headers, data=payload)
      return postOneSpecialty