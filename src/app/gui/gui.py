from app.utils import singleton

@singleton
class Gui(object):
   main = None
   user = None
   user_type = None

   def boot(self, main):
      self.main = main
   def run(self):
      self.main.show()