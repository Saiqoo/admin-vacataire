BEGIN TRANSACTION;
DROP TABLE IF EXISTS "comptes";
CREATE TABLE IF NOT EXISTS "comptes" (
	"login"	VARCHAR(8),
	"mdp"	VARCHAR(128),
	"role"	VARCHAR(15) NOT NULL,
	PRIMARY KEY("login")
);
DROP TABLE IF EXISTS "enseignants";
CREATE TABLE IF NOT EXISTS "enseignants" (
	"id_enseignant"	INTEGER,
	"nom"	VARCHAR(50) NOT NULL,
	"prenom"	VARCHAR(50) NOT NULL,
	"email"	VARCHAR(100) NOT NULL UNIQUE,
	"tel"	VARCHAR(10),
	"login"	VARCHAR(8),
	PRIMARY KEY("id_enseignant"),
	FOREIGN KEY("login") REFERENCES "comptes"("login")
);
DROP TABLE IF EXISTS "modules";
CREATE TABLE IF NOT EXISTS "modules" (
	"intitule"	VARCHAR(20) NOT NULL,
	"abbr"	VARCHAR(150),
	"code_module"	VARCHAR(20) NOT NULL,
	PRIMARY KEY("code_module")
);
DROP TABLE IF EXISTS "vacataires";
CREATE TABLE IF NOT EXISTS "vacataires" (
	"id_vacataire"	INTEGER,
	"nom"	VARCHAR(50) NOT NULL,
	"prenom"	VARCHAR(50) NOT NULL,
	"email"	VARCHAR(100) NOT NULL UNIQUE,
	"tel"	VARCHAR(10),
	"statut"	VARCHAR(100) NOT NULL,
	"employeur"	VARCHAR(200),
	"login"	VARCHAR(8),
	"recrutable"	BOOLEAN,
	PRIMARY KEY("id_vacataire"),
	FOREIGN KEY("login") REFERENCES "comptes"("login")
);
DROP TABLE IF EXISTS "contrats";
CREATE TABLE IF NOT EXISTS "contrats" (
	"id_contrat"	INTEGER,
	"date_deb"	DATE UNIQUE,
	"date_fin"	DATE CHECK(DATE("date_deb") < DATE("date_fin")) UNIQUE,
	"id_vacataire"	INTEGER UNIQUE,
	"id_referent"	INTEGER UNIQUE,
	PRIMARY KEY("id_contrat"),
	FOREIGN KEY("id_vacataire") REFERENCES "vacataires"("id_vacataire"),
	FOREIGN KEY("id_referent") REFERENCES "enseignants"("id_enseignant")
);
DROP TABLE IF EXISTS "interventions";
CREATE TABLE IF NOT EXISTS "interventions" (
	"id_contrat"	INTEGER,
	"code_module"	VARCHAR(20),
	"nbre_heures"	FLOAT,
	FOREIGN KEY("code_module") REFERENCES "modules"("code_module"),
	FOREIGN KEY("id_contrat") REFERENCES "contrats"("id_contrat")
);
COMMIT;
