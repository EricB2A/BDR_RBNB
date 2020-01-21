from app.gui.page import Page
from app.gui.gui import Gui
from app.db.entity_manager import EntityManager
from .mode_select import mode_select_page
from app.entities.personne import Personne
import logging

def login_():
   em = EntityManager()
   db = em.get_db()
   userId = -1
   while "Verfication de l'utilisateur":
      try:
         username  = input("Email: ")
         password = input("Password: ")

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

