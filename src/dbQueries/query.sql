    
-- utiliser pour connaitre les fourniture de l'appartement
select nom_fourniture from search_biens sb
	INNER JOIN fourniture f ON sb.id = f.bien_immobilier_id

