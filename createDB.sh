#!/bin/bash

#this doesn't seem to work on a raspberry Pi
#need to update for postgresql anyway


#This script creates the database schema to allow
#data loading later

if [[ $# -ne 1]]; then
    echo "Usage: createDB.sh dbfile.db"
    exit
fi

sqlite3 $1 <<EOF
CREATE TABLE IF NOT EXISTS SyringePumps (
    Address TEXT, /*The pump's logical address*/
    Name TEXT, /*The pump's name*/
    MaxVolume REAL, /*The maximum volume of the syringe*/
    VolPercent REAL, /*The percentage of paint left in syringe*/
    Rate REAL, /*The unitless rate at which the pumps dispenses*/
    Units TEXT /*The volume and rate units specified in the docs*/
);
EOF

#initial schematic
CREATE TABLE Runs(
    Id INT PRIMARY KEY NOT NULL,
    Name TEXT
);

CREATE TABLE Commands(
    TimePoint DECIMAL NOT NULL,
    CNCComm TEXT,
    RAComm TEXT,
    SYRComm TEXT,
    RUN_ID INT references Runs(Id)
)

#eventual schematic
CREATE TABLE Runs(
    Id INT PRIMARY KEY NOT NULL,
    Name TEXT,
    DateTime TIMESTAMP
);

CREATE TABLE RunData(
    Timepoint DECIMAL NOT NULL,
    SysPos_ID INT references SystemPositions(Id),
    CNCComm_ID INT references CNCCommands(Id),
    SrvComm_ID INT references ServoCommands(Id),
    PmpComm_ID INT references PumpCommands(Id),
    RUN_ID INT references Runs(Id)
);

CREATE TABLE SystemPositions(
    Id INT PRIMARY KEY NOT NULL,

);

CREATE TABLE CNCCommands(
    Id INT PRIMARY KEY NOT NULL,

);

CREATE TABLE ServoCommands(
    Id INT PRIMARY KEY NOT NULL,

);

CREATE TABLE PumpCommands(
    Id INT PRIMARY KEY NOT NULL,

)