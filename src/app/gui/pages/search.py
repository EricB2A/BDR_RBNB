from app.gui.page import Page
from app.db.entity_manager import EntityManager

from entities.type_bien import TypeBien

import app.gui.pages.inquirer as inquirer

from pprint import pprint
from datetime import datetime
from datetime import timedelta
import termtables as tt
import mysql.connector
from app.utils.path import get_config_path
import json
import logging
from app.gui.gui import Gui

config = {}
with open(get_config_path("db.json"),"r") as f:
   config = json.load(f)

db = mysql.connector.connect(**config)

def search_():
   # permet d'envoyer une requete et renvoie le résultat
   def getQueryRes(query):
      cu = db.cursor()
      cu.execute(query)
      return cu.fetchall()
   # permet d'insérer les résultat au moyen d'une requete 
   def insert(query):
      cu = db.cursor()
      cu.execute(query)
      db.commit()
      logging.debug(cu.statement)
      return cu.rowcount is 1

   # ajouter une query
   def addAndToQuery(query, fieldName, value):
         if query:
            query += " AND {} = '{}'".format(fieldName, value)
         else: 
            query = " {} = '{}'".format(fieldName, value)
         return query

   # permet de créer une requete where avec les fields spécifier
   def createWhere(choices, field, binaryOp="OR"):
      firstLoop = True
      query = ""
      for choice in choices.get('interests'):
         if not firstLoop:
            query += " {} ".format(binaryOp)
         query += "{} = '{}'".format(field, choice)
         firstLoop = False

      return query

   # permet de créer le where de l'adresse / position de bien
   def createWherePosition(answers):
      query = ""
      if answers.get('pays'): 
         query = "pays='{}'".format(answers.get('pays'))

      if answers.get('commune'):
         query = addAndToQuery(query, "commune", answers.get('commune'))

      if answers.get('postalCode'):
         query = addAndToQuery(query, "npa", answers.get('postalCode'))
      return query

   # https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float
   def isNumber(s):
      try:
         int(s)
         return True
      except ValueError:
         return False
   # use to check date
   def isValidDate(date):
      try:         
         datetime.strptime(date,'%d/%m/%Y')
         return True
      except ValueError:
         return False
   
   # use to check user date input
   def isValidDateOrNone(date):
      if date:
         return isValidDate(date)
      else:
         return True
   # demande la date
   def askDate(canBeNull=True):
      startDate = ""
      duration = -1
      while "check date is empty or valid":
         dateCriteria = inquirer.prompt([
            inquirer.Text('startDate', message="Entrez une date de début", validate=lambda x: isValidDateOrNone(x))
         ])
         startDateStr = dateCriteria.get('startDate')
         # Si l'utilisateur fournit une date on lui force à mettre une durée
         if startDateStr:
            startDate = datetime.strptime(startDateStr,'%d/%m/%Y')
            durationCriteria = inquirer.prompt([
               inquirer.Text('duration', message="Entrez une durée (nombre de jours)",
               validate=lambda x: isNumber(x) and int(x) > 0),
            ])
            duration = int(durationCriteria.get('duration'))
            break
         else:
            if canBeNull:
               break    
         print("la date doit être au format jour/mois/annee => eg: 12/12/2020")
      
      return startDate, duration
   def isNumberOrQ(number, maxIdx):
      return (isNumber(number) and int(number) > 0 and int(number) <= maxIdx) or str(number) is "Q"

   def createSearchQuery(fournitreWhere, typeBienWhere, positionWhere, unavailableBienQuery):
    
      searchQuery = "SELECT * FROM search_biens"
      # Si il y a des fourniture, on fait un jointure
      if fournitreWhere:
         searchQuery += " INNER JOIN fourniture ON bien_id = bien_immobilier_id"


      # Si il y a des critères à la recherche on ajoute le mot clé WHERE à la requête
      if fournitreWhere or positionWhere or typeBienWhere or unavailableBienQuery:        
         searchQuery += " WHERE "

      whereQuery = ""

      # On ajoute les différents critères à la requête
      if fournitreWhere:
         whereQuery += fournitureWhere
      
      if typeBienWhere:
         if whereQuery:
            whereQuery = "(" + whereQuery + ") AND (" + typeBienWhere + ")"
         else:
            whereQuery +=  typeBienWhere 


      if positionWhere:
         if whereQuery:
            whereQuery = "(" + whereQuery + ") AND (" + positionWhere + ")"
         else:
            whereQuery +=  positionWhere

      if unavailableBienQuery:
         if whereQuery:
            whereQuery = "(" + whereQuery + ") AND (" + unavailableBienQuery + ")"
         else:
            whereQuery +=  unavailableBienQuery
         
      
      
      return searchQuery + whereQuery

   # TYPE DE BIEN
   bienChoices = inquirer.prompt([
      inquirer.Checkbox('interests',
                      message="Quel genre de bien cherchez-vous ?",
                      choices=list(map(lambda bien : bien[0], getQueryRes("SELECT * FROM type_bien")))),
   ])


   # FOURNITURE 
   fournitureChoices = inquirer.prompt([
      inquirer.Checkbox('interests',
                      message="Quel genre de fourniture sont nécessaire pour vous ?",
                      choices=list(map(lambda type : type[0], getQueryRes("SELECT nom FROM type_fourniture")))),
   ])

   print("\n")

   positionCriteria = inquirer.prompt([
      inquirer.Text('pays', message="Entrez un pays"),
      inquirer.Text('commune', message="Entrez une commune"),
      inquirer.Text('postalCode', message="Entrez une NPA")
   ])
   
   positionWhere = createWherePosition(positionCriteria)

   typeBienWhere = createWhere(bienChoices, "type_bien")
   fournitureWhere = createWhere(fournitureChoices, "nom_fourniture", "OR")
   fournitureQuery = ""
   if fournitureWhere:
      fournitureQuery = "bien_id IN (SELECT bien_immobilier_id FROM fourniture WHERE {} GROUP BY bien_immobilier_id HAVING COUNT(*) = {})".format(fournitureWhere, len(fournitureChoices.get('interests')))

   startDate = ""
   duration = ""
   startDate, duration = askDate()

   unavailableBienQuery = ""
   if startDate:
      endDate = startDate + timedelta(days=duration)
      sqlStartDate = startDate.strftime('%Y-%m-%d') # date, pas datetime
      sqlEndDate = endDate.strftime('%Y-%m-%d')
      print()
      unavailableBienQuery = "bien_id NOT IN (SELECT DISTINCT bien_immobilier_id FROM location WHERE (date_arrivee BETWEEN '{}' AND '{}') OR (DATE_ADD(date_arrivee, INTERVAL duree DAY) BETWEEN '{}' AND '{}') AND estConfirme = 1) ".format(sqlStartDate, sqlEndDate, sqlStartDate, sqlEndDate)

   searchQuery = createSearchQuery(fournitureQuery, typeBienWhere, positionWhere, unavailableBienQuery)
   print(searchQuery)   
   input("att")
  
   goodsRes = getQueryRes(searchQuery)
   if(len(goodsRes) == 0):
      print("Aucun resultat")
      input("Tappez une touche pour continuer")
      return False

   
   headerBiens = ["Indice ", "ID", "Cap. person.", "Taille (m²)", "type_bien", "Description", "Rue","Commune", "Etat"]
   
   # affichage des résultat
   while True:
      biens = []
      Page.clear()
      idx = 1
      for good in goodsRes:
         biens.append([idx, good[0], good[2], good[1], good[5], good[3], good[9], good[7], good[8]])
         idx = idx + 1
      
      print( tt.to_string(
            data=biens,
            header=headerBiens,
            style=tt.styles.ascii_thin_double,
         ))
      bienIdx = inquirer.prompt([inquirer.Text('bienIdx',
                  message="Sélectionnez un bien (ou q pour quitter) ", validate=lambda idx: isNumberOrQ(idx, len(goodsRes))
               )])
      bienIdx = bienIdx["bienIdx"]
      
      # afficher un bien ou quitter
      if bienIdx is "Q":
         return False

      idx = int(bienIdx)

      idx = idx - 1
      
      fournitures = getQueryRes("SELECT * FROM fourniture WHERE bien_immobilier_id = {}".format(goodsRes[idx][0]))

      print("Info appartement ----------------")
      print("id du bien : {}".format(goodsRes[idx][0]))
      print("Capacite personne : {}".format(goodsRes[idx][2]))
      print("Taille (m²) : {}".format(goodsRes[idx][1]))
      print("Type bien: {}".format(goodsRes[idx][5]))
      print("Description: {}".format(goodsRes[idx][3]))
      print("Tarif: {}".format(goodsRes[idx][13]))
      print("Charge: {}".format(goodsRes[idx][14]))
      print("Adresse: {} {} {} {} {}".format(goodsRes[idx][9], goodsRes[idx][11], goodsRes[idx][12], goodsRes[idx][7], goodsRes[idx][4]))
      if fournitures:
         print("Fournitures Disponbiles: ")
         for fourniture in fournitures:
            print(" -" + fourniture[3])

      # réserver ? 
      reserver = inquirer.prompt([inquirer.Text("ouiNon", message="Souhaitez-vous réserver ce bien (O/N) ?", 
                                 validate=lambda x: x is "O" or x is "N")])
      
      # si O on réserve autrement on réaffiche les résultats
      if reserver.get('ouiNon') is "O":
         if startDate == "": 
            startDate, duration = askDate(False)
         
         g = Gui()
         goodIdx = bienIdx - 1  

         isAlreadyRented = getQueryRes("SELECT bien_est_occupe({},'{}',{})".format(goodsRes[bienIdx][0], startDate, duration))
         
         print("resultat fonction sql {}".format(isAlreadyRented[0][0]))
         query = "INSERT INTO location(date_arrivee, duree, estConfirme, locataire_id, bien_immobilier_id) VALUES('{}',{}, NULL,{},{})".format(startDate, duration, g.user.id, goodsRes[goodIdx][0])
         logging.debug(query)

         if not isAlreadyRented[0][0] and insert(query):
            print("Votre réservation à bien été faite...") 
            input("Appuyez sur une touche")
            return True
         else:
            print("Bien indisponible")
            input("Appuyez sur une touche")
            return False
         



# Search page
search = Page("search", title="Rechercher un bien")
search.set_main(search_)