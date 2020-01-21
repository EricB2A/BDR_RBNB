-- Fonction pour inserer une nouvelle location
DELIMITER//
CREATE FUNCTION insert_location(loc_id int, bien_immo_id int, date_arrivee date, duree int)
RETURN boolean

END //

