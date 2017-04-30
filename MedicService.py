from flask import Flask, request
from Medic import * 
import requests
import json

class MedicService:

   def getAllMedic(self,token):
      url = "http://gsb-planning-api/admin/medics"
      headers = {'authorization': token,
                  'Connection':'keep-alive'}
      allMedic = requests.get(url, headers=headers)
      return allMedic.json()

   def getOneMedic(self,token, id):
      url = "http://gsb-planning-api/admin/medics/"+str(id)
      headers = {'authorization': token,
                  'Connection':'keep-alive'}
      OneMedic = requests.get(url, headers=headers)
      return OneMedic.json()


   def putOneMedic(self, token, medic):
      url = "http://gsb-planning-api/admin/medics/"+str(medic.id)
      payload = medic.dictionarize()
      del payload['id']
      headers = {'authorization': token,
                  'Content-Type': 'application/x-www-form-urlencoded'}
      putOneMedic = requests.put(url, headers=headers, data=payload)
      return putOneMedic

   def deleteOneMedic(self,token, key):
      url = "http://gsb-planning-api/admin/medics/"+str(key)
      headers = {'authorization': token}
      deleteOneMedic = requests.delete(url, headers=headers)
      return deleteOneMedic

   def createOneMedic(self, token, medic):
      url = "http://gsb-planning-api/admin/medics"
      payload = medic.dictionarize()
      del payload['id']
      headers = {'authorization': token,
                  'Content-Type': 'application/x-www-form-urlencoded'}
      postOneMedic = requests.post(url, headers=headers, data=payload)
      return postOneMedic