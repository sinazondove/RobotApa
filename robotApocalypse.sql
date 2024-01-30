-- Database: robotApocalypse

-- DROP DATABASE IF EXISTS "robotApocalypse";
-- Table to track the status of survivors' conditions
CREATE TABLE Survivor_Status (
    survivor_id INT PRIMARY KEY,
    infected BOOLEAN NOT NULL,
    times_reported_infected INT DEFAULT 0,
    FOREIGN KEY (survivor_id) REFERENCES Survivors(survivor_id)
);
