# Projet BDR - Schéma relationnel
pays( <u>nom</u> )

commune(<u>nom</u>, etat, nom_pays, pays_nom)  
commune.pays_nom <i>référence</i> pays.nom

adresse(<u>id</u>, rue, complementRue, numero, npa, nom_commune)
rue, npa NOT NULL    
adresse.nom_commune <i>référence</i> commune.nom

personne(<u>id</u>, nom, prenom, email, motDePasse, genre, adresse_id)
nom, prenom, email, mot_de_passe NOT NULL
email UNIQUE  

type_bien(<u>nom</u>)  

bien_immobilier(<u>id</u>, taille, capacite, description, tarif_journalier, 
charges, adresse_id, nom_type_bien_nom, proprietaire_id)  
charges, tarif_journalier NOT NULL  
bien_immobilier.proprietaire_id <i>référence</i> Personne.id  
bien_immobilier.adresse_id <i>référence</i> Adresse.id  
bien_immobilier.type_bien_nom <i>référence</i> type_bien.nom  

type_fourniture(<u>nom</u>)

fourniture(<u>id</u>, description, nom_type_fourniture, bien_immobilier_id)  
bien_immobilier_id, nom_fourniture NOT NULL
fourniture.nom_type_fourniture <i>référence</i> Type_fourniture.nom 
fourniture.bien_immobilier_id <i>référence</i> Bien_immobilier.id

location(<u>id</u>, date_arrivee, duree, estConfirme, bien_immobilier_id, locataire_id)  
location.bien_immobilier_id <i>référence</i> bien_immobilier.id
location.locataire_id <i>référence</i> personne.id

review(<u>id</u>, note, commentaire, location_id)
note NOT NULL
review.location_id <i>référence</i> location.id

message(<u>id</u>, contenu, location_id, author_id)  
location_id, author_id NOT NULL
message.author_id <i>référence</i> personne.id
meessage.location_id <i>référence</i> location.id

 
 
 
 
