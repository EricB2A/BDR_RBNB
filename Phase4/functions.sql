use airbnb;

-- Fonction qui vérifie si deux périodes se chevauchent

DROP FUNCTION IF EXISTS dates_superposees;
DELIMITER //
CREATE FUNCTION dates_superposees(date1 DATE, date2 DATE, duree1 int, duree2 int)
RETURNS boolean
DETERMINISTIC
BEGIN
DECLARE reponse boolean;
    IF (date1 BETWEEN date2 AND ADDDATE(date2, duree2)
        OR ADDDATE(date2, duree2) BETWEEN date1 AND ADDDATE(date1, duree1)
        OR date2 BETWEEN date1 AND ADDDATE(date1, duree1)) THEN
        SET reponse = TRUE;
    ELSE
        SET reponse = FALSE;
    END IF;
RETURN reponse;
END //
DELIMITER ;



-- Vérifie si une location a déjà lieu dans l'intervalle donnée.
DROP FUNCTION IF EXISTS bien_est_libre;
DELIMITER //
CREATE FUNCTION bien_est_libre(
    bien_id INT,
    starting_date DATE,
    duration INT
)
RETURNS BOOL
READS SQL DATA
BEGIN
    RETURN NOT EXISTS(
        SELECT l.id FROM location as l
        WHERE l.bien_immobilier_id = bien_id
        AND ((l.date_arrivee BETWEEN starting_date AND DATE_ADD(starting_date, INTERVAL duration DAY)
        OR (DATE_ADD(l.date_arrivee, INTERVAL duration DAY) BETWEEN starting_date AND
        DATE_ADD(starting_date, INTERVAL duration DAY) )
        OR DATE_ADD(starting_date, INTERVAL duration DAY) BETWEEN l.date_arrivee AND DATE_ADD(l.date_arrivee, INTERVAL duration DAY))
        AND l.estConfirme = 1)
    );
END //

DELIMITER ;
