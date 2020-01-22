from app.gui.page import Page
from app.gui.gui import Gui
from app.entities.personne import Personne
from app.utils.path import get_config_path
import app.gui.pages.inquirer as inquirer
import logging
from .adresse import get_address
from app.entities.addrese import Addresse
import json
import mysql.connector
import functools
config = {}
with open(get_config_path("db.json"),"r") as f:
   config = json.load(f)

db = mysql.connector.connect(**config)

profil_page = Page("Profile")

def change_address():
   g = Gui()
   current_user = g.user
   query = "DELETE FROM adresse WHERE id = {}".format(current_user.adresse_id)
   logging.debug("EXECUTING QUERY: %s", query)
   cursor = db.cursor()
   cursor.execute(query)
   db.commit()
   if cursor.rowcount > 0:
      address = Addresse.create(**get_address())
      current_user.adresse_id = address.id
      current_user.save()
      print("Mise à jour de l'adresse effectué!")
   else:
      print("Impossible de mettre à jour l'adresse actuel")
   Page.wait_input()
   return True

def change_password():
   g = Gui()
   current_user = g.user

   questions = [
      inquirer.Password("password", message="nouveau mot de passe")
   ]
   answers = inquirer.prompt(questions)
   if "password" not in answers.keys():
      return False
   query = "UPDATE personne SET mot_de_passe='{}' WHERE id = {}".format(answers["password"], current_user.id)
   logging.debug("QUERY: %s", query)
   cursor = db.cursor()
   cursor.execute(query)
   db.commit()
   if cursor.rowcount > 0:
      print("Mot de passe mis à jour")
   else:
      print("Echec de la mise à jour")
   Page.wait_input()
   return True

def change_email():
   g = Gui()
   current_user = g.user

   questions = [
      inquirer.Text("email", message="nouvelle email")
   ]
   answers = inquirer.prompt(questions)
   if "email" not in answers.keys():
      return False
   email = answers["email"]
   if len(Personne.where("`email`='{}'".format(email))) > 0:
      print("Un utilisateur possède déjà cette email...")
      Page.wait_input()
      return False

   query = "UPDATE personne SET email='{}' WHERE id = {}".format(answers["email"], current_user.id)
   logging.debug("QUERY: %s", query)
   cursor = db.cursor()
   cursor.execute(query)
   db.commit()
   if cursor.rowcount > 0:
      print("Email mis à jour")
   else:
      print("Echec de la mise à jour")
   Page.wait_input()
   return True

def change_data():
   g = Gui()
   current_user = g.user
   questions = [
      inquirer.Text("nom", message="Nouveau nom"),
      inquirer.Text("prenom", message="Nouveau prénom"),
      inquirer.List("genre", message="Genre", choices=["Homme", "Femme", "Agender", "Pangender", "Androgyne", "Genre fluide"], default=current_user.genre)
   ]
   answers = inquirer.prompt(questions)
   if "genre" not in answers.keys():
      return False

   
   fields = { k:v for k,v in answers.items() if v}

   if len(fields.keys()) <= 0:
      return False
   set_query = "SET "
   for k,v in fields.items():
      set_query += "{} = '{}', ".format(k,v)
   query = "UPDATE personne {} WHERE id = {}".format(set_query[:-2], current_user.id)
   logging.debug("QUERY: %s", query)
   cursor = db.cursor()
   cursor.execute(query)
   db.commit()
   if cursor.rowcount > 0:
      print("Mot de passe mis à jour")
   else:
      print("Echec de la mise à jour")
   Page.wait_input()
   return True
   print("Mise à jour de vos donnée personnel effectué avec succès")
   Page.wait_input()

profil_page.append_item(change_data, "Changer nom/prénom/genre ")
profil_page.append_item(change_email, "Changer d'email")
profil_page.append_item(change_password, "Changer de mot de passe")
profil_page.set_next(profil_page)