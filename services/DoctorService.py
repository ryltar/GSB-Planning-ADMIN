from flask import Flask, request
from Doctor import * 
import requests
import json

class DoctorService:

   def getAllDoctor(self,token):
      url = "http://claudioppe.ddns.net/admin/doctors"
      headers = {'authorization': token,
                  'Connection':'keep-alive'}
      allDoctor = requests.get(url, headers=headers)
      return allDoctor.json()

   def getOneDoctor(self,token, id):
      url = "http://claudioppe.ddns.net/admin/doctors/"+str(id)
      headers = {'authorization': token,
                  'Connection':'keep-alive'}
      OneDoctor = requests.get(url, headers=headers)
      return OneDoctor.json()


   def putOneDoctor(self, token, doctor):
      url = "http://claudioppe.ddns.net/admin/doctors/"+str(doctor.id)
      payload = doctor.dictionarize()
      del payload['id']
      headers = {'authorization': token,
                  'Content-Type': 'application/x-www-form-urlencoded'}
      putOneDoctor = requests.put(url, headers=headers, data=payload)
      return putOneDoctor.json()

   def deleteOneDoctor(self,token, key):
      url = "http://claudioppe.ddns.net/admin/doctors/"+str(key)
      headers = {'authorization': token}
      deleteOneDoctor = requests.delete(url, headers=headers)
      return deleteOneDoctor.json()

   def createOneDoctor(self, token, doctor):
      url = "http://claudioppe.ddns.net/admin/doctors"
      payload = doctor.dictionarize()
      print(payload)
      del payload['id']
      headers = {'authorization': token,
                  'Content-Type': 'application/x-www-form-urlencoded'}
      postOneDoctor = requests.post(url, headers=headers, data=payload)
      print(postOneDoctor)
      return postOneDoctor