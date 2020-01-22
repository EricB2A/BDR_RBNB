
import termtables as tt
import logging
import json
import mysql.connector

from app.entities.bien_immobilier import BienImmobilier
from app.entities.type_bien import TypeBien
from app.entities.addrese import Addresse

from app.gui.page import Page
from app.gui.gui import Gui

from app.utils.path import get_config_path
import app.gui.pages.inquirer as inquirer

from .adresse import get_address

config = {}
with open(get_config_path("db.json"),"r") as f:
   config = json.load(f)

db = mysql.connector.connect(**config)


def building_modal(building = None):
   existed = False
   if building is None:
      building = BienImmobilier()
   else:
      building = BienImmobilier.find(building["bien_id"])
      existed = True
   type_bien = TypeBien.find()

   type_bien_default = building.type_bien_nom if building.exists else None

   fields = [
      inquirer.RequiredText("description", message = "Description"),
      inquirer.Numeric("charges", message="Charges"),
      inquirer.Numeric("tarif_journalier", message="Tarifs journaliers"),
      inquirer.Numeric("capacite", message="Capacité"),
      inquirer.Numeric("taille", message="Taille"),
      inquirer.List("type_bien_nom", message="Type de bien", choices=list(map(lambda x: x.nom,type_bien)), default=type_bien_default)
   ]

   if building.exists:
      msg_address = "Voulez vous changer l'adresse actuel"
      fields.append(inquirer.Confirm("address_change", message=msg_address))

   answers = inquirer.prompt(fields)
   if answers is None:
      return False

   answers = { k:v for k,v in answers.items() if str(v).strip() } #filter out empty answers
   if not len(answers.keys()):
      return False
   
   if building.exists and answers["address_change"] is True:
      query = "SET FOREIGN_KEY_CHECKS=0; DELETE FROM adresse WHERE id = {}; SET FOREIGN_KEY_CHECKS=1;".format(building.adresse_id)
      cursor = db.cursor()
      logging.debug("QUERY: %s", query)
      for res in cursor.execute(query, multi=True):
         pass
      db.commit()
      building.adresse_id = None

   # saving part
   g = Gui()
   current_user = g.user
   data_for_building = {k:v for k,v in answers.items() if k is not "address_change"}
   building._fill(**data_for_building)
   
   if not building.exists:
      try:
         address_data = get_address()
         address = Addresse.create(**address_data)
         building.adresse_id = address.id
         building.proprietaire_id = current_user.id
         building.save()
         print("Bien immobilier crée correctement")
         return True
      except Exception as e:
         logging.debug(e)
         print("Impossible d'insérer le bien immobilier")
         return False
   else:
      try:
         if answers["address_change"]:
            address_data = get_address()
            address = Addresse.create(**address_data)
            building.adresse_id = address.id
         
         building.proprietaire_id = current_user.id
         building.save()
         print("Bien immobilier mis à jour correctement")
         return True
      except Exception as e:
         logging.debug(e)
         print("Impossible d'insérer le bien immobilier")
         return False

def my_properties_():
   Page.clear()

   g = Gui()
   current_user = g.user
   logging.debug("Current user id %s",current_user.id)
   #Print my buildings
   cursor = db.cursor(dictionary=True)
   query = "SELECT * FROM search_biens WHERE proprietaire = {}".format(current_user.id)
   logging.debug("QUERY: %s", query)
   cursor.execute(query)
   my_rentals = cursor.fetchall()
   db.commit()
   logging.debug(my_rentals)
   headers = [
      "id", "Type de bien", "description", "addresse"
   ]
   def build_addresse(ad):
      if ad is None:
         return ""
      return ""+ ad["rue"] + " " + ad["numero"] + " " + ad["etat"] + "(" + ad["commune"] + ")"

   data = list(map(lambda x: (x["bien_id"], x["type_bien"], x["description"][:20], build_addresse(x)),my_rentals))
   if len(data) <= 0:
      data = [ [ "" for i in range(len(headers)) ]] 
   string = tt.to_string(
         data,
         header=headers,
         style=tt.styles.ascii_thin_double,
   )
   print(string)
   
   #Actions on buildings
   mapping_actions={
      "Créer un nouveau bien":"create",
      "Mettre à jour un bien": "update",
      "Supprimer un bien": "delete",
      "Retour":"return"
   }
   actions = [
      inquirer.List("action", message="Que voulez vous faire?", choices=["Créer un nouveau bien", "Mettre à jour un bien", "Supprimer un bien", "Retour"])
   ]
   action = inquirer.prompt(actions)
   logging.debug("CHOOSING TO DO %s ON BUILDING", action)
   if action is None or "action" not in action.keys():
      return False
   
   action = mapping_actions[action["action"]]
   if action == "return":
      return False

   if action == "create":
      b = building_modal()
      if b:
         print("Nouvelle imeuble créé!")
         Page.wait_input()
      return True

   building_id = input("\n Numéro du bien: ")
   if not len(building_id):
      return False
   building_id = int(building_id)
   building_by_id = { x["bien_id"]:x for x in my_rentals }
   logging.debug("MES APPARTEMENTS %s",building_by_id)

   if building_id not in building_by_id.keys():
      print("Vous ne pouvez editer ce bien.")
      Page.wait_input()
      return False

   current_building = building_by_id[building_id]
   if action == "update":
      
      building_modal(current_building)
      Page.wait_input()
   elif action == "delete":
      #get building
      query = "DELETE from bien_immobilier WHERE id = {}".format(building_id)
      logging.debug("QUERY: %s", query)
      cursor = db.cursor()
      cursor.execute(query)
      try:
         db.commit()
         if cursor.rowcount > 0:
            print("Bien immobilier supprimé avec succès")
            return True
         else:
            print("Impossible de supprimer le bien immobilier")
            return False
      except:
         db.rollback()
      Page.wait_input()

def waiting_rentals():
   Page.clear()

   g = Gui()
   current_user = g.user
   logging.debug("Current user id %s",current_user.id)
   #Print my buildings
   cursor = db.cursor(dictionary=True)
   query = "SELECT *, location.id location_id, location.date_arrivee, DATE_ADD(location.date_arrivee, INTERVAL location.duree DAY) date_depart FROM location_prioprietaire INNER JOIN location on location.bien_immobilier_id = location_prioprietaire.bien_id WHERE proprietaire_id = {} AND estConfirme IS NULL AND location.date_arrivee > NOW()".format(current_user.id)
   logging.debug("QUERY: %s", query)
   cursor.execute(query)
   my_rentals = cursor.fetchall()
   db.commit()
   logging.debug("LOCATION EN ATTENTE : %s",my_rentals)
   headers = [
      "id", "Type de bien", "description", "addresse", "date arrivée", "date départ"
   ]
   def build_addresse(ad):
      if ad is None:
         return ""
      return ""+ ad["rue"] + " " + ad["numero"] + " " + ad["etat"] + "(" + ad["commune"] + ")"

   data = list(map(lambda x: (x["bien_id"], x["type_bien"], x["description"][:20], build_addresse(x), x["date_arrivee"], x["date_depart"]),my_rentals))
   if len(data) <= 0:
      data = [ [ "" for i in range(len(headers)) ]] 
   string = tt.to_string(
         data,
         header=headers,
         style=tt.styles.ascii_thin_double,
   )
   print(string)
   
   #Actions on buildings
   mapping_actions={
      "Valider la location":"accept",
      "Refuser la location": "refuse",
      "Retour":"return"
   }
   actions = [
      inquirer.List("action", message="Que voulez vous faire?", choices=["Valider la location", "Refuser la location", "Retour"])
   ]
   action = inquirer.prompt(actions)
   logging.debug("CHOOSING TO DO %s ON BUILDING", action)
   if action is None or "action" not in action.keys():
      return False
   
   action = mapping_actions[action["action"]]
   if action == "return":
      return False

   #Check that it actually is our building
   building_id = input("\n Numéro du bien: ")
   if not len(building_id):
      return False

   building_id = int(building_id)
   building_by_id = { x["bien_immobilier_id"]:x for x in my_rentals }
   logging.debug(building_by_id)
   if building_id not in building_by_id.keys():
      print("Vous ne pouvez editer ce bien.")
      Page.wait_input()
      return False
   #Build query
   query = ""
   if action == "refuse":
      query = "UPDATE location SET `estConfirme`=0 WHERE bien_immobilier_id = {}".format(building_id)
   elif action == "accept":
      query = "UPDATE location SET `estConfirme`=1 WHERE bien_immobilier_id = {}".format(building_id)

   logging.debug("QUERY: %s", query)
   cursor = db.cursor()
   cursor.execute(query)
   try:
      db.commit()
      if cursor.rowcount > 0:
         print("Location mis à jour avec succès")
         return True
      else:
         print("Impossible de mettre à jour la location")
         return False
   except:
      db.rollback()
   Page.wait_input()


def rentals_now():
   Page.clear()

   g = Gui()
   current_user = g.user
   logging.debug("Current user id %s",current_user.id)
   #Print my buildings
   cursor = db.cursor(dictionary=True)
   query = "SELECT *, location.id location_id, location.date_arrivee, DATE_ADD(location.date_arrivee, INTERVAL location.duree DAY) date_depart FROM location_prioprietaire INNER JOIN location on location.bien_immobilier_id = location_prioprietaire.bien_id WHERE proprietaire_id = {} AND estConfirme = 1 AND DATE(NOW()) BETWEEN location.date_arrivee AND DATE_ADD(location.date_arrivee, INTERVAL location.duree DAY) ".format(current_user.id)
   logging.debug("QUERY: %s", query)
   cursor.execute(query)
   my_rentals = cursor.fetchall()
   db.commit()
   logging.debug("LOCATION EN ATTENTE : %s",my_rentals)
   headers = [
      "id", "Type de bien", "description", "addresse", "date arrivée", "date départ"
   ]
   def build_addresse(ad):
      if ad is None:
         return ""
      return ""+ ad["rue"] + " " + ad["numero"] + " " + ad["etat"] + "(" + ad["commune"] + ")"

   data = list(map(lambda x: (x["bien_id"], x["type_bien"], x["description"][:20], build_addresse(x), x["date_arrivee"], x["date_depart"]),my_rentals))
   if len(data) <= 0:
      data = [ [ "" for i in range(len(headers)) ]] 
   string = tt.to_string(
         data,
         header=headers,
         style=tt.styles.ascii_thin_double,
   )
   print(string)
   
   #Actions on buildings
   mapping_actions={
      "Retour":"return"
   }
   actions = [
      inquirer.List("action", message="Que voulez vous faire?", choices=["Retour"])
   ]
   action = inquirer.prompt(actions)
   logging.debug("CHOOSING TO DO %s ON BUILDING", action)
   if action is None or "action" not in action.keys():
      return False
   
   action = mapping_actions[action["action"]]
   if action == "return":
      return False


def rentals_before():
   Page.clear()

   g = Gui()
   current_user = g.user
   logging.debug("Current user id %s",current_user.id)
   #Print my buildings
   cursor = db.cursor(dictionary=True)
   query = "SELECT *, location.id location_id, location.date_arrivee, DATE_ADD(location.date_arrivee, INTERVAL location.duree DAY) as date_depart FROM location_prioprietaire INNER JOIN location on location.bien_immobilier_id = location_prioprietaire.bien_id WHERE proprietaire_id = {} AND estConfirme = 1 AND location.date_arrivee < DATE(NOW())".format(current_user.id)
   logging.debug("QUERY: %s", query)
   cursor.execute(query)
   my_rentals = cursor.fetchall()
   db.commit()
   logging.debug("LOCATION EN ATTENTE : %s",my_rentals)
   headers = [
      "id", "Type de bien", "description", "addresse", "date arrivée", "date départ"
   ]
   def build_addresse(ad):
      if ad is None:
         return ""
      return ""+ ad["rue"] + " " + ad["numero"] + " " + ad["etat"] + "(" + ad["commune"] + ")"

   data = list(map(lambda x: (x["bien_id"], x["type_bien"], x["description"][:20], build_addresse(x), x["date_arrivee"], x["date_depart"]),my_rentals))
   if len(data) <= 0:
      data = [ [ "" for i in range(len(headers)) ]] 
   string = tt.to_string(
         data,
         header=headers,
         style=tt.styles.ascii_thin_double,
   )
   print(string)
   
   #Actions on buildings
   mapping_actions={
      "Retour":"return"
   }
   actions = [
      inquirer.List("action", message="Que voulez vous faire?", choices=["Retour"])
   ]
   action = inquirer.prompt(actions)
   logging.debug("CHOOSING TO DO %s ON BUILDING", action)
   if action is None or "action" not in action.keys():
      return False
   
   action = mapping_actions[action["action"]]
   if action == "return":
      return False

def rentals_future():
   Page.clear()

   g = Gui()
   current_user = g.user
   logging.debug("Current user id %s",current_user.id)
   #Print my buildings
   cursor = db.cursor(dictionary=True)
   query = "SELECT *, location.id location_id, location.date_arrivee, DATE_ADD(location.date_arrivee, INTERVAL location.duree DAY) date_depart FROM location_prioprietaire INNER JOIN location on location.bien_immobilier_id = location_prioprietaire.bien_id WHERE proprietaire_id = {} AND estConfirme = 1 AND DATE_ADD(location.date_arrivee, INTERVAL location.duree DAY) > DATE(NOW())".format(current_user.id)
   logging.debug("QUERY: %s", query)
   cursor.execute(query)
   my_rentals = cursor.fetchall()
   db.commit()
   logging.debug("LOCATION EN ATTENTE : %s",my_rentals)
   headers = [
      "id", "Type de bien", "description", "addresse", "date arrivée", "date départ"
   ]
   def build_addresse(ad):
      if ad is None:
         return ""
      return ""+ ad["rue"] + " " + ad["numero"] + " " + ad["etat"] + "(" + ad["commune"] + ")"

   data = list(map(lambda x: (x["bien_id"], x["type_bien"], x["description"][:20], build_addresse(x), x["date_arrivee"], x["date_depart"]),my_rentals))
   if len(data) <= 0:
      data = [ [ "" for i in range(len(headers)) ]] 
   string = tt.to_string(
         data,
         header=headers,
         style=tt.styles.ascii_thin_double,
   )
   print(string)
   
   #Actions on buildings
   mapping_actions={
      "Refuser la location": "refuse",
      "Retour":"return"
   }
   actions = [
      inquirer.List("action", message="Que voulez vous faire?", choices=["Refuser la location", "Retour"])
   ]
   action = inquirer.prompt(actions)
   logging.debug("CHOOSING TO DO %s ON BUILDING", action)
   if action is None or "action" not in action.keys():
      return False
   
   action = mapping_actions[action["action"]]
   if action == "return":
      return False

   #Check that it actually is our building
   building_id = input("\n Numéro du bien: ")
   if not len(building_id):
      return False
   building_id = int(building_id)
   building_by_id = { x["bien_immobilier_id"]:x for x in my_rentals }
   logging.debug(building_by_id)
   if building_id not in building_by_id.keys():
      print("Vous ne pouvez editer ce bien.")
      Page.wait_input()
      return False
   #Build query
   query = ""
   if action == "refuse":
      query = "UPDATE location SET `estConfirme` = NULL WHERE bien_immobilier_id = {}".format(building_id)

   logging.debug("QUERY: %s", query)
   cursor = db.cursor()
   cursor.execute(query)
   try:
      db.commit()
      if cursor.rowcount > 0:
         print("Location mis à jour avec succès")
         return True
      else:
         print("Impossible de mettre à jour la location")
         return False
   except:
      db.rollback()
   Page.wait_input()
my_properties = Page("my_properties", title="Gérer mes biens")
my_properties.set_main(my_properties_)
my_properties.set_next(my_properties)

pending_locations = Page("pending_rentals", title="Locations en attente")
pending_locations.set_main(waiting_rentals)
pending_locations.set_next(pending_locations)

rentals_occuring_now = Page("rentals_occuring_now", title="Locations en cours")
rentals_occuring_now.set_main(rentals_now)


rentals_in_the_past = Page("past_rentals", title="Locations terminées")
rentals_in_the_past.set_main(rentals_before)

rentals_in_the_future = Page("future_rentals", title="Locations qui vont arriver")
rentals_in_the_future.set_main(rentals_future)

manage_properties = Page("manage_properties", title="Gérer mes propriétés")
manage_properties.append_item(my_properties)
manage_properties.append_item(pending_locations)
manage_properties.append_item(rentals_occuring_now)
manage_properties.append_item(rentals_in_the_past)
manage_properties.append_item(rentals_in_the_future)