# Projet BDR - Schéma relationnel
Pays( <u>nom</u> )
Commune(<u>nom</u>, etat, nom_pays)
Adresse(<u>id</u>, rue, complementRue, numero, npa, nom_commune)
Personne(<u>id</u>, nom, prenom, email, motDePasse, genre, adresse_id)
TypeBien(<u>nom</u>)
BienImmobilier(<u>id</u>, taille, capacite, description, tarifJournalier, charges)
TypeFourniture(<u>nom</u>)
Fourniture(<u>id</u>, description)
Location(<u>id</u>, date, duree, estConfirme)
Review(<u>id</u>, note, commentaire)
Message(<u>id</u>, contenu)

