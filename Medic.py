class Medic:

    def __init__(self, med_info=[]):
        try:
            self.id = med_info['id']
            self.name = med_info['lib']
            self.description = med_info['description']
        except:
            self.id = None
            self.name = None
            self.description = None

    def dictionarize(self):
        return {'id': self.id,
                'lib': self.name,
                'description': self.description}
