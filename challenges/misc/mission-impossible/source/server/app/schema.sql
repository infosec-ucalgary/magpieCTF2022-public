DROP TABLE IF EXISTS Connections;
DROP TABLE IF EXISTS Lasers;
DROP TABLE IF EXISTS Requests;

CREATE TABLE Connections (
    IP          TEXT,
    First_time  INTEGER,
    Attempts    INTEGER,
    PRIMARY KEY (IP)
);

CREATE TABLE Lasers (
    Name    TEXT,
    State   INTEGER,
    PRIMARY KEY (Name)
);

CREATE TABLE Requests (
    Id  TEXT,
    Timestamp   REAL,
    Laser0   INTEGER,
    Laser1   INTEGER,
    Laser2   INTEGER,
    Laser3   INTEGER,
    PRIMARY KEY (Id)
);

INSERT INTO Lasers VALUES ("Laser0", 1);
INSERT INTO Lasers VALUES ("Laser1", 1);
INSERT INTO Lasers VALUES ("Laser2", 1);
INSERT INTO Lasers VALUES ("Laser3", 1);
