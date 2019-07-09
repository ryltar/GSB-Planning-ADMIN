class Address:

    def __init__(self, add_info=[]):
        try:
            self.id = add_info["id"]
            self.num = add_info["num"]
            self.street = add_info["street"]
            self.codepost = add_info["codepost"]
            self.city = add_info["city"]
            self.country = add_info["country"]
            self.indication = add_info["indication"]

        except:
            self.id = None
            self.num = None
            self.street = None
            self.codepost = None
            self.city = None
            self.country = None
            self.indication = None

    def dictionarize(self):
        return {'id': self.id,
                'num': self.num,
                'street': self.street,
                'codepost': self.codepost,
                'city': self.city,
                'country': self.country,
                'indication': self.indication}
