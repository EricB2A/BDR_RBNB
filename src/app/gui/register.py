import inquirer
import logging
from ..entities.user import User
from .page import Page
from .gui import Gui
from .page_repository import main
from .mode_select import mode_select_page
def register_():
   print("Hello new user, please fill out the following form \n\n")
   entity = User()
   answers = None
   fields = [
      "nom",
      "prenom",
      "genre",
   ]
   questions = list(map(lambda f: inquirer.Text(f, message="{}".format(f)), fields))
   questions.append(inquirer.Text("email","Email"))
   questions.append(inquirer.Password("password", message="Mot de passe"))

   while "Create a user uniquely with his email":
      answers = inquirer.prompt(questions)
      if answers is None:
         return False
      #check if user doesn't aready exist
      #TODO change he email field to actual email table field
      if len(User.where("`email` = '{}'".format(answers["email"]))) > 0: 
         print("A user with the email {} already exists....".format(answers["email"]))
         input("Press enter to continue...")
      else:
         break

   logging.debug("Creating user (%s) with values %s", entity, answers)
   
   for field, value in answers.items():
      setattr(entity, field, value)
   
   return entity.save()

register_page = Page("Enregistrer un nouvelle utilisateur")
register_page.set_main(register_)
register_page.set_next(mode_select_page)


if __name__ == "__main__":
   mode_select_page.show()