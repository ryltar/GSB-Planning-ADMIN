class Employee:

   def __init__(self, emp_info=[]):
      try:
         self.admin = emp_info["is_admin"]
         self.email = emp_info["email"]
         self.id = emp_info["id"]
         self.lastname = emp_info["lastname"]
         self.phone = emp_info["num_tel"]
         self.pseudo = emp_info["pseudo"]
         self.firstname = emp_info["firstname"]

      except:
         self.admin = None
         self.lastname = None
         self.firstname = None
         self.pseudo = None
         self.email = None
         self.phone = None
         self.id = None
         self.password = None

   def dictionarize(self):
      if hasattr(self, 'password'):
        return {'id': self.id,
                'is_admin': self.admin,
                'lastname': self.lastname,
                'firstname': self.firstname,
                'pseudo': self.pseudo,
                'email': self.email,
                'num_tel': self.phone,
                'passwd': self.password}
      else:
        return {'id': self.id,
                'is_admin': self.admin,
                'lastname': self.lastname,
                'firstname': self.firstname,
                'pseudo': self.pseudo,
                'email': self.email,
                'num_tel': self.phone}
