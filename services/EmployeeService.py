from flask import Flask, request
from Employee import * 
import requests
import json

class EmployeeService:

   def getAllEmployee(self,token):
      url = "http://claudioppe.ddns.net/admin/employees"
      headers = {'authorization': token,
                  'Connection':'keep-alive'}
      allEmployee = requests.get(url, headers=headers)
      return allEmployee.json()

   def getOneEmployee(self,token, id):
      url = "http://claudioppe.ddns.net/admin/employees/"+str(id)
      headers = {'authorization': token,
                  'Connection':'keep-alive'}
      OneEmployee = requests.get(url, headers=headers)
      return OneEmployee.json()


   def putOneEmployee(self, token, employee):
      url = "http://claudioppe.ddns.net/admin/employees/"+str(employee.id)
      payload = employee.dictionarize()
      del payload['id']
      headers = {'authorization': token,
                  'Content-Type': 'application/x-www-form-urlencoded'}
      putOneEmployee = requests.put(url, headers=headers, data=payload)
      return putOneEmployee

   def deleteOneEmployee(self,token, key):
      url = "http://claudioppe.ddns.net/admin/employees/"+str(key)
      headers = {'authorization': token}
      deleteOneEmployee = requests.delete(url, headers=headers)
      return deleteOneEmployee

   def createOneEmployee(self, token, employee):
      url = "http://claudioppe.ddns.net/admin/employees"
      payload = employee.dictionarize()
      print(payload)
      del payload['id']
      headers = {'authorization': token,
                  'Content-Type': 'application/x-www-form-urlencoded'}
      postOneEmployee = requests.post(url, headers=headers, data=payload)
      print(postOneEmployee)
      return postOneEmployee


   