from app.utils import singleton
from .page_repository import login

@singleton
class Gui(object):
   main = login
   
   user = None
   user_type = None

   def boot(self):
      pass
   def run(self):
      self.main.show()