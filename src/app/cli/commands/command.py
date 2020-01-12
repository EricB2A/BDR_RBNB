from abc import abstractmethod

class Command:
   """
   Base class for any command in the app.
   The command is passed arguments for what to do on init and on run
   """
   command_name = None
   def __init__(*args, **kwargs):
      pass

   def help(self):
      pass

   @abstractmethod
   def run(self, *args):
      """
      This function receives a list of arguments provided from sys.argv
      """
      pass