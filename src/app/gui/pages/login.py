from app.gui.page import Page
from app.gui.gui import Gui
from app.db.entity_manager import EntityManager
from .mode_select import mode_select_page
from app.entities.personne import Personne
import logging
import app.gui.pages.inquirer as inquirer

def login_():
   em = EntityManager()
   db = em.get_db()
   userId = -1
   questions = [
      inquirer.RequiredText("email", "Addresse email"),
      inquirer.Password("password", "Mot de passe")
   ]
   while "Verfication de l'utilisateur":
      try:
         answers = inquirer.prompt(questions)
         if len(answers.keys()) != 2:
            return False
         username = answers["email"]
         password = answers["password"]
         #cuGetTypeBien = db.cursor(dictionary=True)
         users = Personne.where("email= '{}' AND mot_de_passe='{}' LIMIT 0,1".format(username, password))

         #userRes = cuGetTypeBien.fetchall()

         if len(users) == 1:
            g = Gui()
            g.user = users[0]
            userId = users[0].id
            break
         print("L'utilisateur n'existe pas")
      except KeyboardInterrupt:
         return False
   return True

login = Page("Login")
login.set_main(login_)
login.set_next(mode_select_page)

