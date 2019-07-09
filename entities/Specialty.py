class Specialty:

   def __init__(self, spec_info=[]):
      try:
         self.id = spec_info["id"]
         self.label = spec_info["label"]

      except:
         self.id = None
         self.label = None

   def dictionarize(self):
      return {'id': self.id,
              'label': self.label}