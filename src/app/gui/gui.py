from app.utils import singleton
from .page_repository import menuConnectionPage

@singleton
class Gui(object):
   main = menuConnectionPage
   
   user = None
   user_type = None

   def boot(self):
      pass
   def run(self):
      self.main.show()