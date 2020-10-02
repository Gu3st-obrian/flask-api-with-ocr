DROP TABLE IF EXISTS credentials;
CREATE TABLE credentials (
	idcredential INTEGER PRIMARY KEY AUTOINCREMENT,
	label TEXT NOT NULL,
	dbhost TEXT NOT NULL,
	dbuser TEXT NOT NULL,
	dbpass TEXT NOT NULL,
	dbname TEXT NOT NULL
);
