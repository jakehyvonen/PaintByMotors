#!/bin/bash
#This is the only way I could get psql to work in a shell script
sudo -i -u postgres -- psql -c "CREATE DATABASE adatabase;"
sudo -i -u postgres -- psql -c "CREATE TABLE atable;"