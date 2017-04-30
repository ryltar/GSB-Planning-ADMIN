class Doctor:

    def __init__(self, doc_info=[]):
        try:
            self.id = doc_info['id']
            self.lastname = doc_info['lastname']
            self.firstname = doc_info['firstname']
            self.num_tel = doc_info['num_tel']
            self.email = doc_info['email']
            self.employee = doc_info['id_employee']
            self.address = doc_info['id_address']
            self.specialty = doc_info['id_specialty']
        except:
            self.id = None
            self.lastname = None
            self.firstname = None
            self.num_tel = None
            self.email = None
            self.address = None
            self.employee = None
            self.specialty = None

    def dictionarize(self):
        return {'id': self.id,
                'lastname': self.lastname,
                'firstname': self.firstname,
                'num_tel': self.num_tel,
                'email': self.email,
                'id_employee': self.employee,
                'id_address': self.address,
                'id_specialty': self.specialty}