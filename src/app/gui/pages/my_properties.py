from app.gui.page import Page
from app.gui.gui import Gui
import termtables as tt
import logging
import app.gui.pages.inquirer as inquirer
from app.entities.bien_immobilier import BienImmobilier
from app.entities.type_bien import TypeBien
from app.entities.addrese import Addresse
from app.entities.commune import Commune
import json
import mysql.connector
from app.utils.path import get_config_path

config = {}
with open(get_config_path("db.json"),"r") as f:
   config = json.load(f)

db = mysql.connector.connect(**config)

def _get_address():
   communes = Commune.find()
   commune_mapping = { x.nom + "(" + x.pays_nom + ")":x.nom for x in communes }
   fields = [
      inquirer.Text("rue", message="Rue"),
      inquirer.Text("complement_rue", message="Complément"),
      inquirer.Text("numero", message="Numéro"),
      inquirer.Text("npa", message="Npa"),
      #inquirer.Text("ville", message="Ville"),
      inquirer.List("commune_nom", message="Commune", choices=list(commune_mapping.keys()))
   ]
   answers = inquirer.prompt(fields)
   if answers is None:
      return None
   answers["commune_nom"] = commune_mapping[answers["commune_nom"]]
   return answers

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
      inquirer.Text("description", message = "Description"),
      inquirer.Text("charges", message="Charges"),
      inquirer.Text("tarif_journalier", message="Tarifs journaliers"),
      inquirer.Text("capacite", message="Capacité"),
      inquirer.Text("taille", message="Taille"),
      inquirer.List("type_bien_nom", message="Type de bien", choices=list(map(lambda x: x.nom,type_bien)), default=type_bien_default)
   ]

   if building.exists:
      msg_address = "Voulez vous changer l'adresse actuel"
      fields.append(inquirer.Confirm("address_change", message=msg_address))

   answers = inquirer.prompt(fields)
   if answers is None:
      return False
   answers = { k:v for k,v in answers.items() if str(v).strip() } #filter out empty answers
   data_for_building = {k:v for k,v in answers.items() if k is not "address_change"}
   building._fill(**data_for_building)

   if building.exists and answers["address_change"] is True:
      building.addresse.delete() #destroy the current address   
   # saving part
   g = Gui()
   current_user = g.user

   if not building.exists:
      try:
         address_data = _get_address()
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
            address_data = _get_address()
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
   my_buildings = cursor.fetchall()
   db.commit()
   logging.debug(my_buildings)
   headers = [
      "id", "Type de bien", "description", "addresse"
   ]
   def build_addresse(ad):
      if ad is None:
         return ""
      return ""+ ad["rue"] + " " + ad["numero"] + " " + ad["etat"] + "(" + ad["commune"] + ")"

   data = list(map(lambda x: (x["bien_id"], x["type_bien"], x["description"][:20], build_addresse(x)),my_buildings))
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
      "Supprimer un bien": "delete"

   }
   actions = [
      inquirer.List("action", message="Que voulez vous faire?", choices=["Créer un nouveau bien", "Mettre à jour un bien", "Supprimer un bien"])
   ]
   action = inquirer.prompt(actions)
   logging.debug("CHOOSING TO DO %s ON BUILDING", action)
   if action is None:
      return False
   
   action = mapping_actions[action["action"]]

   if action == "create":
      b = building_modal()
      if b:
         print("Nouvelle imeuble créé!")
      return True

   building_id = input("\n Numéro du bien: ")
   building_id = int(building_id)
   building_by_id = { x["bien_id"]:x for x in my_buildings }
   logging.debug(building_by_id)
   if building_id not in building_by_id.keys():
      print("Hey you're trying to update something that isn't yours fuck off")
      input(">")
      return False

   current_building = building_by_id[building_id]
   if action == "update":
      
      building_modal(current_building)
      input("Appuyez sur entrée pour continuer....")
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
      input("Appuyez sur entrée pour continuer....")
   
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