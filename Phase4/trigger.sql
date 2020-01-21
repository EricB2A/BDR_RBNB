--
-- Trigger pour infirmer les locations si une autre à la même date est
-- confirmée
DELIMITER // 
CREATE TRIGGER auto_disable_bien_immo
AFTER UPDATE ON location
FOR EACH ROW BEGIN
    IF (NEW.estConfirme = TRUE) THEN
        UPDATE location SET
        estConfirme = FALSE
        WHERE estConfirme IS NULL 
        AND location.bien_immobilier_id = NEW.bien_immobilier_id
        AND (
            (location.date_arrivee > NEW.date_arrivee AND location.date_arrivee < (NEW.date_arrivee + NEW.duree))
             OR (location.date_arrivee + duree > NEW.date_arrivee AND location.date_arrivee + duree < (NEW.date_arrivee + NEW.duree))
             OR (location.date_arrivee < NEW.date_arrivee AND location.date_arrivee + location.duree > NEW.date_arrivee)
        );
    END IF;
END//
DELIMITER ;

-- Trigger 


