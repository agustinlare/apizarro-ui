UPDATE sreaio.active SET iduser=1, stop_date=NOW() WHERE id=1;

CREATE TABLE active(id INT(11) AUTO_INCREMENT PRIMARY KEY, iduser INT(11), start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, stop_date TIMESTAMP NULL);

ALTER TABLE sreaio.active ADD isActive BOOL DEFAULT True NOT NULL;