from db.entity_manager import EntityManager
import sys
from .commands import available_commands
import logging

class Cli:
   VERSION = "1.0.0"
   def __init__(self, config, entity_manager):
      self.config = config
      self.entity_manager = entity_manager
      logging.debug("IS STILL CONNECTED EM: {}".format(entity_manager))
      logging.debug("Available commands : {}".format(available_commands))

   def _parse_args(self):
      return list(filter(lambda s: not s.startswith("--"),sys.argv[1:]))

   def help(self, path = []):
      command_executable = "{} {}".format(sys.executable, sys.argv[0])
      usage = "{} [command]".format(command_executable)

      if len(path) <= 0:
         command_available = ""
         for c in available_commands.keys():
            command_available += ("\t" + c + "\n")
         print("""
Airbnb cli version {}
Usage: {}
Available commands:
{}
         """.format(self.VERSION, usage, command_available))
      elif len(path) >= 1 and len(path) <= 2:
         if path[0] in available_commands.keys():
            available_commands[path[0]].help()
         else:
            print("Command not found")
            self.help()
      # elif len(path) == 2:
      #    print("Print help on action + entity, which means interogating entity manager to see what we can do")
      else:
         print("all hell broke loose hallelujah")

   def get_action(self, args):
      logging.debug("Arguments for app : %s", args)
      return (
         args[0] if len(args) > 0 else "",
         args[1:] if len(args) > 1 else []
      )

   def run(self):
      #arguments have the following format
      # (action) (entity) (any other needed arguments)
      # action represents anything the cli can do
      # entity provides where to execute the action, if needed
      # the rest of the arguments are supplied to the callee function
      (name, arguments) = self.get_action(self._parse_args())

      logging.debug("Trying to run command ".format(name))
      if name in available_commands.keys():
         command = available_commands[name](*arguments)
         command.run(*arguments)
         sys.exit(0)
         return 0
      
      if len(arguments) <= 2:
         self.help(arguments)
         sys.exit(2)
         return
      
      if name not in available_commands.keys():
         print("Command not found")
         self.help()
         sys.exit(2)
         return
      

      print("Fatal error")
      sys.exit(2)
      
