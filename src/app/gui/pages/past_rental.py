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

config = {}
with open(get_config_path("db.json"),"r") as f:
   config = json.load(f)
   
db = mysql.connector.connect(**config)

def getQueryRes(query):
    cu = db.cursor(dictionary=True)
    cu.execute(query)
    return cu.fetchall()

def displayRental():
    g = Gui()
    # a ajouter avant where 
    query = "SELECT * FROM location_personne INNER JOIN search_biens ON bien_immobilier_id = search_biens.bien_id WHERE DATE_ADD(location_personne.date_arrivee, INTERVAL location_personne.duree DAY) < NOW() AND location_personne.estConfirme = TRUE AND personne_id = {}".format(g.user.id) 
    locations = getQueryRes(query)
    headerBiens = ["Cap. person.", "Taille (m²)", "type_bien", "Description", "Rue","Commune", "Etat", "date arrivee", "date depart"]

    
    biens = []
    for location in locations:
        biens.append([location["capacite"], location["taille"], location["type_bien"], location["description"], location["rue"], location["commune"], location["etat"],location["date_arrivee"],location["date_depart"] ])

    if biens:
        print( tt.to_string(
                data=biens,
                header=headerBiens,
                style=tt.styles.ascii_thin_double,
             ))
    input("Appuyez sur une touche")
    return True

PastRental = Page("Past Rental")
PastRental.set_main(displayRental)

