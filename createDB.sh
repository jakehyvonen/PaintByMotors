#!/bin/bash

#This script creates the database schema to allow
#data loading later

if [[$# -ne 1]]; then
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
)