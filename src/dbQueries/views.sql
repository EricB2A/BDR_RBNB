
-- RECHERCHE
CREATE VIEW `search_biens` AS 
    SELECT bi.id 'bien_id', taille, capacite, description, p.nom 'pays',tb.nom 'type_bien' ,
           proprio.nom , c.nom 'commune', etat, rue, complement_rue, ville,
		   numero, npa, bi.tarif_journalier, bi.charges
    FROM bien_immobilier bi
        -- relatif à postion/adresse complète de l'appartement
        INNER JOIN adresse a ON bi.adresse_id = a.id
        INNER JOIN commune c ON a.commune_nom = c.nom
        INNER JOIN pays p ON c.pays_nom = p.nom 
        -- relatif au type de bien
        INNER JOIN type_bien tb ON bi.type_bien_nom = tb.nom
        -- relatif au proprio
        INNER JOIN personne proprio ON bi.proprietaire_id = proprio.id;
        
        
    