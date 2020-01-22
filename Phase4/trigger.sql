use airbnb;

-- Trigger pour infirmer les locations si une autre à la même date est confirmée.
DELIMITER //
DROP TRIGGER IF EXISTS auto_disable_bien_immo;
CREATE TRIGGER auto_disable_bien_immo
AFTER UPDATE ON location
FOR EACH ROW BEGIN
    IF (NEW.estConfirme = TRUE) THEN
        UPDATE location
        SET estConfirme = FALSE
        WHERE estConfirme IS NULL
        AND location.bien_immobilier_id = NEW.bien_immobilier_id
        AND (
            (location.date_arrivee > NEW.date_arrivee AND location.date_arrivee < (NEW.date_arrivee + NEW.duree))
             OR (location.date_arrivee + duree > NEW.date_arrivee AND location.date_arrivee + duree < (NEW.date_arrivee + NEW.duree))
             OR (location.date_arrivee < NEW.date_arrivee AND location.date_arrivee + location.duree > NEW.date_arrivee)
        );
    END IF;
END//

-- CI: Une review ne peut être faite qu'une fois la date de fin de réservation (date + duree) passée.
DROP TRIGGER IF EXISTS ci_revue_apres_fin_location;
CREATE TRIGGER ci_revue_apres_fin_location
BEFORE INSERT ON review
FOR EACH ROW BEGIN
    IF(EXISTS(SELECT DATE_ADD(l.date_arrivee, INTERVAL l.duree DAY) FROM location as l WHERE l.id = NEW.location_id AND DATE_ADD(l.date_arrivee, INTERVAL l.duree DAY) >= CURDATE())) THEN
        signal sqlstate '45000';
    END IF;
END//

-- CI: Si une Personne envoi un Message, alors ce dernier doit être le Propriétaire ou le Locataire de la Location.
DROP TRIGGER IF EXISTS ci_envoi_messaage;
CREATE TRIGGER ci_envoi_messaage
BEFORE INSERT ON message
FOR EACH ROW BEGIN
    IF(NOT EXISTS(
    SELECT l.locataire_id FROM location as l
    INNER JOIN bien_immobilier as bi ON l.bien_immobilier_id = bi.id
    WHERE l.id = NEW.location_id
    AND (NEW.author_id = l.locataire_id OR NEW.author_id = bi.proprietaire_id)
    ))THEN
        signal sqlstate '45000';
    END IF;

END//




DELIMITER ;

-- Trigger
