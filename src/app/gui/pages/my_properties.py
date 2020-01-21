from app.gui.page import Page
from app.gui.gui import Gui
import termtables as tt
import logging
import inquirer
from app.entities.bien_immobilier import BienImmobilier
from app.entities.type_bien import TypeBien
from app.entities.commune import Commune
import json
import mysql.connector
from app.utils.path import get_config_path

config = {}
with open(get_config_path("db.json"),"r") as f:
   config = json.load(f)

db = mysql.connector.connect(**config)

#TODO redo with queries
def _get_address(building = None):
   communes = Commune.find()

   fields = [
      inquirer.Text("rue", message="Rue"),
      inquirer.Text("complement_rue", message="Complément"),
      inquirer.Text("numero", message="Numéro"),
      inquirer.Text("npa", message="Npa"),
      inquirer.Text("ville", message="Ville"),
      inquirer.List("commune_nom", message="Commune", choices=list(map(lambda x: x.nom,communes)))
   ]
   return fields

def building_modal(building = None):
   if building is None:
      building = BienImmobilier()
   type_bien = TypeBien.find()
   fields = [
      inquirer.Text("charge", message="Charge"),
      inquirer.Text("tarif_journalier", message="Tarifs journaliers"),
      inquirer.Text("description", message = "Description"),
      inquirer.Text("capacite", message="Capacité"),
      inquirer.Text("taille", message="Taille"),
      inquirer.List("type_bien_nom", message="Type de bien", choices=list(map(lambda x: x.nom,type_bien)))
      
   ]
   if building.exists:
      msg_address = "Voulez vous changer l'adresse actuel"
      fields.append(inquirer.Confirm("address_change", message=msg_address))

   answers = inquirer.prompt(fields)
   building._fill(answers)

   if building.exists and answers["address_change"] is True:
      building.addresse.delete() #destroy the current address   

   if not building.exists or ("address_change" in answers.keys() and answers["address_change"] is True):
      address_data = inquirer.prompt(_get_address(building))
      address = Address.create(address_data)
      building.address = address
      building.save()

def my_properties_():
   Page.clear()

   g = Gui()
   current_user = g.user
   logging.debug("Current user id %s",current_user.id)
   
   my_buildings = BienImmobilier.where("`proprietaire_id` = {}".format(current_user.id))
   actions = [
      inquirer.List("action", message="Que voulez vous faire?", choices=[("Supprimer un bien", "delete"), ("Mettre à jour un bien", "update"), ("Créer un nouveau bien","create")])
   ]
   action = inquirer.prompt(actions)

   if action is None:
      return False
   
   action = action["action"]

   if action == "create":
      b = building_modal()
      return True

   building_id = input("\n Numéro du bien: ")
   building_by_id = { x.id:x for x in my_buildings }

   if building_id not in building_by_id.keys():
      print("Hey you're trying to update something that isn't yours fuck off")
      input(">")
      return False

   current_building = building_by_id[building_id]
   if action == "update":
      
      building_modal(current_building)
   elif action == "delete":
      #get building
      current_building.delete()

   input(">")
my_properties = Page("my_properties", title="Gérer mes biens")
my_properties.set_main(my_properties_)

pending_locations = Page("pending_locations", title="Locations en attente")

manage_properties = Page("manage_properties", title="Gérer mes propriétés")
manage_properties.append_item(my_properties)
manage_properties.append_item(pending_locations)

#En mode Locataire
#Afficher les locations passé
#Afficher les locations futurs
#Manager mes biens --> seulement proprio