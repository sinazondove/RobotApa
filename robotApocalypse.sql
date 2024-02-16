-- Database: robotApocalypse

-- DROP DATABASE IF EXISTS "robotApocalypse";
-- Table to track the status of survivors' conditions
CREATE TABLE Survivor_Status (
    survivor_id INT PRIMARY KEY,
    infected BOOLEAN NOT NULL,
    times_reported_infected INT DEFAULT 0,
    FOREIGN KEY (survivor_id) REFERENCES Survivors(survivor_id)
);
-- Table to store resources possessed by survivors
CREATE TABLE Survivor_Resources (
    resource_id INT PRIMARY KEY AUTO_INCREMENT,
    survivor_id INT,
    water INT DEFAULT 0,
    food INT DEFAULT 0,
    medication INT DEFAULT 0,
    ammunition INT DEFAULT 0,
    FOREIGN KEY (survivor_id) REFERENCES Survivors(survivor_id)
);