use airbnb;

INSERT 
INTO pays (nom)
VALUES
    ("Suisse"),
    ("France"),
    ("Belgique"),
    ("Allemagne"),
    ("Grande-Bretagne"),
    ("Italie"),
    ("Espagne"),
    ("Portugal"),
    ("Autriche"),
    ("Grèce"),
    ("Pologne"),
    ("Suède"),
    ("Norvège"),
    ("Finlande"),
    ("Russie"),
    ("USA"),
    ("Mexique"),
    ("Brésil"),
    ("Pérou"),
    ("Colombie"),
    ("Marco"),
    ("Tunisie"),
    ("Turquie"),
    ("Egypte"),
    ("Chine"),
    ("Japon"),
    ("Thailande"),
    ("Ukraine"),
    ("Israel"),
    ("Palestine")
;

INSERT
INTO commune (nom, etat, pays_nom)
VALUES
    ("Yverdon-les-Bains", "Vaud", "Suisse"),
    ("Lausanne", "Vaud", "Suisse"),
    ("Montreux", "Vaud", "Suisse"),
    ("Nyon", "Vaud", "Suisse"),
    ("Neuchatel", "Neuchatel", "Suisse"),
    ("La Chaux-de-Fonds", "Neuchatel", "Suisse"),
    ("Le Locle", "Neuchatel", "Suisse"),
    ("Delemont", "Jura", "Suisse"),
    ("Porrentruy", "Jura", "Suisse"),
    ("Saignelegier", "Jura", "Suisse"),
    ("Geneve", "Geneve", "Suisse"),
    ("Vernier", "Geneve", "Suisse"),
    ("Sion", "Valais", "Suisse"),
    ("Martigny", "Valais", "Suisse"),
    ("Crans-Montana", "Valais", "Suisse"),
    ("Bern", "Bern", "Suisse"),
    ("Bienne", "Bern", "Suisse"),
    ("Zurich", "Zurich", "Suisse"),
    ("Winterthour", "Zurich", "Suisse"),
    ("Paris", "Seine", "France"),
    ("Marseille", "Bouches-du-Rhone", "France"),
    ("Lyon", "Rhone", "France"),
    ("Nice", "Alpes-Maritimes", "France"),
    ("Toulouse", "Haute-Garonne", "France"),
    ("Bordeaux", "Gironde", "France"),
    ("Berlin", "Berlin", "Allemagne"),
    ("Hambourg", "Hambourg", "Allemagne"),
    ("Munich", "Baviere", "Allemagne")
;


INSERT
INTO adresse (commune_nom, rue, complement_rue, numero, npa)
VALUES
    ("Yverdon-les-Bains", "Route de Cheseaux", NULL, "1", "CH-1401"),
    ("Yverdon-les-Bains", "Rue de la Plaine", NULL, "68", "CH-1400"),
    ("Yverdon-les-Bains", "Rue des Prés-du-Lac", NULL, "21B", "CH-1400"),
    ("Lausanne", "Chemin de la Lisière", NULL, "8", "CH-1018"),
    ("Lausanne", "Chemin de la Lisière", NULL, "25A", "CH-1018"),
    ("Lausanne", "Chemin du Reposoir", NULL, "1", "CH-1007"),
    ("Montreux", "Rue de l'Ancien Stand", NUll, "28", "CH-1820"),
    ("Nyon", "Rue de la Combe", NULL, "12", "CH-1260"),
    ("Neuchatel", "Faubourg du Lac", NULL, "31", "CH-2000"),
    ("Neuchatel", "Faubourg de l'Hopital", NULL, "13", "CH-2000"),
    ("La Chaux-de-Fonds", "Rue du Progres", NULL, "7", "CH-2300"),
    ("La Chaux-de-Fonds", "Rue du Temple Allemand", NULL, "5", "CH-2300"),
    ("Le Locle", "Avenue du College", NULL, "6A", "CH-2400"),
    ("Delemont", "Rue de Morepont", NULL, "5", "CH-2800"),
    ("Saignelegier", "Rue de la Gruere", NULL, "10", "CH-2350"),
    ("Geneve", "Rue des Maraichers", NULL, "11", "CH-1205"),
    ("Geneve", "Rue des Maraichers", NULL, "15", "CH-1205"),
    ("Geneve", "Route de Frontenex", NULL, "122", "CH-1208"),
    ("Sion", "Rue de l'Avenir", NULL, "25", "CH-1950"),
    ("Sion", "Avenue Ritz", NULL, "25", "CH-1950"),
    ("Sion", "Rue du Grand Pont", NULL, "17", "CH-1950"),
    ("Bienne", "Chemin des Landes", NULL, "2", "CH-2503"),
    ("Paris", "Boulevard Rocheouart", NULL, "32", "75018"),
    ("Paris", "Boulevard Magenta", NULL, "115", "75010"),
    ("Paris", "Rue Lourmel", NULL, "48B", "75015")
;


INSERT
INTO personne (nom, prenom, email, mot_de_passe, adresse_id, genre)
VALUES 
    ("Baxter","Joel","Phyllis@Ut.org","at", 2, "Homme"),
    ("Hampton","Peter","Phillip@ut.us","tempor", 7, "Homme"),
    ("Kirk","Tanek","Keane@lectus.edu","mus", 6, "Homme"),
    ("Ortega","Henry","Lisandra@eros.edu","ac", 1, "Homme"),
    ("Lawrence","Burke","Bradley@Praesent.us","nascetur", 9, "Homme"),
    ("Barber","Adena","Jarrod@facilisis.com","pretium", 12, "Femme"),
    ("Coleman","Herrod","Urielle@a.edu","hendrerit", 22, "Homme"),
    ("Wyatt","Erin","Bert@conubia.us","neque", 25, "Femme"),
    ("Haley","Demetrius","Avram@aptent.org","dis", 15, "Homme"),
    ("Glover","Cathleen","Medge@a.net","gravida", 13, "Femme"),
    ("Landry","Stephen","Meredith@amet.gov","montes", 11, "Homme"),
    ("Oliver","Deirdre","Rhoda@eget.com","fermentum", 17, "Homme"),
    ("Randolph","Cecilia","Alexis@Duis.org","arcu", 7, "Femme"),
    ("Lott","Caldwell","Raphael@metus.net","nisi", 8, "Homme"),
    ("Potts","Jenette","Jackson@nisi.us","Lorem", 21, "Femme"),
    ("Guerrero","Wing","Alvin@eros.org","tellus", 19, "Homme"),
    ("Mendez","Kirk","Whilemina@ridiculus.com","tincidunt", 15, "Homme"),
    ("Garrison","Leigh","Kane@eros.edu","Pellentesque", 14, "Homme"),
    ("Spears","Rigel","Hyatt@bibendum.org","Maecenas", 14, "Homme"),
    ("Cox","Eagan","Sylvester@mattis.com","blandit", 4, "Homme"),
    ("Barnett","Serena","Lionel@Praesent.edu","taciti", 24, "Femme"),
    ("Young","Julie","Katelyn@porta.net","orci", 16, "Femme"),
    ("Day","Brennan","Abdul@Nam.com","hymenaeos", 16, "Homme"),
    ("Zimmerman","Regina","Finn@accumsan.net","magna", 23, "Femme"),
    ("Joyner","Unity","Keefe@risus.us","placerat", 3, "Femme"),
    ("Lyons","Ann","Carolyn@nulla.us","orci", 23, "Femme"),
    ("Warren","Arsenio","Prescott@Proin.org","volutpat", 24, "Homme"),
    ("Terry","Oprah","Remedios@lorem.gov","nulla", 1, "Femme")
;

INSERT 
INTO type_bien (nom)
VALUES
    ("Studio"),
    ("Appartement"),
    ("Duplex"),
    ("Villa"),
    ("Chalet"),
    ("Cabanon"),
    ("Maison"),
    ("Chambre")
;

INSERT
INTO bien_immobilier (adresse_id, type_bien_nom, proprietaire_id,
                      taille, capacite, description, tarif_journalier,
                      charges)
VALUES
    ((SELECT adresse_id from personne WHERE id = 1), "Studio", 1, 25, 2, "Petit studio sympathique, cuisine, salle de bain.", 43.8, 60.0),
    ((SELECT adresse_id from personne WHERE id = 2), "Appartement", 2, 60, 3, "Appartement lumineux", 72.7, 70.0),
    ((SELECT adresse_id from personne WHERE id = 3), "Appartement", 3, 72, 5, "Appartement tout neuf, bien placé", 120.0, 160.0),
    ((SELECT adresse_id from personne WHERE id = 5), "Studio", 5, 30, 1, "Grand studio", 34.9, 45.0),
    ((SELECT adresse_id from personne WHERE id = 7), "Appartement", 7, 74, 3, "Appartement en centre-ville", 67.0, 80.0),
    ((SELECT adresse_id from personne WHERE id = 12), "Appartement", 12, 80, 5, "Grand appartement pour fêtes", 103.33, 60.0),
    ((SELECT adresse_id from personne WHERE id = 15), "Appartement", 15, 54, 3, "Appartement typique", 35.00, 35.0),
    ((SELECT adresse_id from personne WHERE id = 21), "Villa", 21, 240, 8, "Très grande villa pour vacances de rêves", 350.00, 600.0),
    ((SELECT adresse_id from personne WHERE id = 23), "Chambre", 23, 12, 1, "Chambre de bonne à l'étage", 23.8, 0.0),
    ((SELECT adresse_id from personne WHERE id = 17), "Appartement", 17, 81, 6, "Grand appartement, un peu viellot", 145.5, 120.0),
    ((SELECT adresse_id from personne WHERE id = 13), "Chambre", 13, 10, 1, "Petite chambre", 27.8, 60.0)
;

INSERT
INTO type_fourniture (nom)
VALUES
    ("Cuisine"),
    ("Salon"),
    ("Terrasse"),
    ("Balcon"),
    ("Douche"),
    ("Baignoire"),
    ("Buanderie")
;
INSERT
INTO location (date_arrivee, duree, estConfirme, locataire_id, bien_immobilier_id) 
VALUES 
    ("13.02.2020", 7, false, 8, 11), 
    ("12.07.2020", 7, true, 18, 4), 
    ("15.03.2020", 4, true, 20, 2), 
    ("09.02.2020", 2, true, 4, 7), 
    ("24.07.2020", 7, true, 8, 1), 
    ("24.08.2020", 15, false, 22, 7), 
    ("02.08.2020", 15, true, 12, 8), 
    ("15.04.2020", 8, false, 4, 9), 
    ("14.05.2020", 4, true, 16, 10), 
    ("24.05.2020", 13, false, 19, 11),
    ("20.03.2020", 7, null, 19, 11),
    ("19.03.2020", 13, null, 10, 11)
;

