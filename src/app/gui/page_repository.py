from .page import Page
from db import EntityManager

from entities.type_bien import TypeBien
import inquirer
from pprint import pprint
from datetime import datetime
from datetime import timedelta

import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="airbnb"
)

def creationUser():
   print("creation de l'utilisateur")
   input("attend")
   return True


def login():
   userId = -1
   while "Verfication de l'utilisateur":
      username  = input("Email: ")
      password = input("Password: ")

      cuGetTypeBien = db.cursor()
      cuGetTypeBien.execute("SELECT id FROM personne WHERE email= '{}' AND mot_de_passe='{}'".format(username, password))

      userRes = cuGetTypeBien.fetchall()
      pprint(userRes)
      if len(userRes) != 0:
         userId = userRes[0][0]
         break
      print("L'utilisateur n'existe pas")

   return True

def search_():
   def getQueryRes(query):
      cu = db.cursor()
      cu.execute(query)
      return cu.fetchall()

   def showMultipleChoice(choices):
      for x in choices.get('interests'):
         print(" -"+x)


   def addAndToQuery(query, fieldName, value):
         if query:
            query += " AND {} = '{}'".format(fieldName, value)
         return query

  
   def createWhere(choices, field, binaryOp="OR"):
      firstLoop = True
      query = ""
      for choice in choices.get('interests'):
         if not firstLoop:
            query += " {} ".format(binaryOp)
         query += "{} = '{}'".format(field, choice)
         firstLoop = False

      return query

   def createWherePosition(answers):
      query = ""
      if answers.get('pays'): 
         query = "pays='{}'".format(answers.get('pays'))

      if answers.get('commune'):
         query = addAndToQuery(query, "commune", answers.get('commune'))

      if answers.get('city') :
         query = addAndToQuery(query, "ville", answers.get('city'))

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
         
   
   def createSearchQuery(fournitreWhere, typeBienWhere, positionWhere, unavailableBienQuery):
    
      searchQuery = "SELECT * FROM search_biens"
      # Si il y a des fourniture, on fait un jointure
      if fournitreWhere:
         searchQuery += " INNER JOIN fourniture ON bien_id = bien_immobilier_id"

      # Si il y a des critères à la recherche on ajoute le mot clé WHERE à la requête
      if fournitreWhere or positionWhere or typeBienWhere or unavailableBienQuery:
         print("***")
         print(fournitureChoices)
         print(positionWhere)
         print(typeBienWhere)
         print(unavailableBienQuery)
         searchQuery += " WHERE "
         print("###")

      
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
      inquirer.Text('city', message="Entrez une ville"),
      inquirer.Text('postalCode', message="Entrez une NPA")
   ])
   
   positionWhere = createWherePosition(positionCriteria)
   typeBienWhere = createWhere(bienChoices, "type_bien")
   fournitureWhere = createWhere(fournitureChoices, "nom_fourniture")

   startDate = ""
   duration = ""
   
   while "check date is empty or valid":
      dateCriteria = inquirer.prompt([
         inquirer.Text('startDate', message="Entrez une date de début", validate=lambda _, x: isValidDateOrNone(x))
      ])
      startDateStr = dateCriteria.get('startDate')
      # Si l'utilisateur fournit une date on lui force à mettre une durée
      if startDateStr:
         startDate = datetime.strptime(startDateStr,'%d/%m/%Y')
         durationCriteria = inquirer.prompt([
            inquirer.Text('duration', message="Entrez une durée (nombre de jours)",
            validate=lambda _, x: isNumber(x)),
         ])
         duration = int(durationCriteria.get('duration'))
         break
      else:
         break    
      print("la date doit être au format jour/mois/annee => eg: 12/12/2020")
   
   unavailableBienQuery = ""
   if startDateStr:
      endDate = startDate + timedelta(days=duration)
      sqlStartDate = startDate.strftime('%Y-%m-%d') # date, pas datetime
      sqlEndDate = endDate.strftime('%Y-%m-%d')

      unavailableBienQuery = "bien_id NOT IN (SELECT DISTINCT bien_immobilier_id FROM location WHERE (date_arrivee BETWEEN {} AND {}) AND (DATE_ADD(date_arrivee, INTERVAL duree DAY) BETWEEN {} AND {})) ".format(sqlStartDate, sqlEndDate, sqlStartDate, sqlEndDate)

   # on construit la requête avec toutes les champs de la recherche
   # TODO tester que les interval de temps sont justes 
   searchQuery = createSearchQuery(fournitureWhere, typeBienWhere, positionWhere, unavailableBienQuery)
   print(searchQuery)

   goodsRes = getQueryRes(searchQuery)
   goodsRows = []

   # index en fonction de la position de la vue 
   # 0 => bien_id
   # 1 => taille
   # 2 => capacite
   # 3 => description
   # 4 => pays
   # 5 => type_bien
   # 6 => proprio_nom
   # 7 => commune
   # 8 => etat
   # 9 => rue
   # 10 => complement_rue
   # 11 => ville
   # 12 => numero
   # 13 => npa
   # 14 => tarif journalier 
   # 15 => charges 

   # TODO ATTENTION SI VILLE / CITY disparait, faire - 1 au index à partir de 11
   for good in goodsRes:
      goodId = good[0]
      # goodDisplay = "{}: nombre de places: {} | tarif: {} | charges: {} | Superficie: {} m² | type de bien : {} | adresse: {} {} {} {}".format(good[3], good[2], good[14],good[15],good[1], good[5], good[9], good[12], good[10], good[7]  )
      goodDisplay = "{}: nombre de places: {} | Superficie: {} m² | type de bien : {} | adresse: {} {} {} {}".format(good[3], good[2], good[14], good[5], good[9], good[12], good[10], good[7]  )
      fournitureRes = getQueryRes("SELECT nom_fourniture FROM fourniture WHERE bien_immobilier_id = {}".format(good[0]))
      
      fournitures = ""
      for fourniture in fournitureRes:
         fournitures += fourniture[0]+" "

      avaiblableFourniture = "type de fournitures disponibles: {}".format(fournitures)
      # goodsRows.append(goodDisplay + avaiblableFourniture)
      goodsRows.append(goodDisplay )
   
   goodChoice = inquirer.prompt([
      inquirer.List('interests',
                      message="Résultat de la cherche",
                      choices=goodsRows),
   ])

   # 2h
   # TODO laisser l'utilisateur choisir un appartement 
   # TODO afficher l'appartement avec les infos 
   # TODO faire une location 

   # 2h
   # TODO faire une vue ou plusieurs (locataire / proriétaire) vu pour
      # - voir ses location passé
      # - voir ses locaition en cours 
      # - voir ses location en attente
      # - 

   # 2h
   # TODO faire une procedure pour créer une adresse sans duplication de pays et commune
   # TODO faire une procedure pour vérifier la disponiblité d'un appartement
   # TODO faire une proecdure pour vérifier qu'un utilisateur à pas déjà un appartement en cours de locaition
      # permet qu'il loue la moitié du site, de plus le compte qui loue doit être celui qui va y habiter

   # 2h
   # TODO suppression d'un appartement
      # TODO faire une procedure pour vérifier qu'il n'y a pas de location en cours ou à venir
      # TODO appeler la procédure de suppresion d'adresse 
      # TODO si 1er procedure ok -> soft delete
      #
   
   # 2h30
   # TODO création d'un appartement 
      # TODO le faire de manière séquentielle
         # TODO créer l'appartement (utilisation de création d'adresse)
         # TODO puis demander les fourniture

      # TODO ? procédure ? 

   # 1h 
   # TODO création de l'utilisateur voir ce qui a déjà été fait
   # TODO modifier son profil

 

   input("ATTEND SEARCH")
   return True


# connection page
connectionPage = Page("Connexion")
connectionPage.set_main(login)


# create user page
creationUserPage = Page("Creation utilisateur")
creationUserPage.set_main(creationUser)

# Search page
search = Page("search")
search.set_main(search_)

mainMenuPage = Page("Menu principale", should_exit=True)
mainMenuPage.append_item(search)

connectionPage.set_next(mainMenuPage)
creationUserPage.set_next(mainMenuPage)

login = Page("Login")
login.set_main(login_)
login.set_next(mode_select_page)
