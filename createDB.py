import sqlite3
from os.path import expanduser
from pathlib import Path
home = expanduser('~')
savedir = home + '/SIEData/'
Path(savedir).mkdir(parents=True, exist_ok=True)
dbname = 'test.db'
connectstr = savedir + dbname
print(connectstr)
#run this to create a new SQLite DB
conn = sqlite3.connect(connectstr)
cursor = conn.cursor()
#create a table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Runs(
run_id INTEGER PRIMARY KEY,
run_name TEXT)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS Commands(
    command_id INTEGER PRIMARY KEY,
    timepoint REAL NOT NULL,
    cnc_comm TEXT,
    ra_comm TEXT,
    syr_comm TEXT
)
""")
conn.commit()
#insert default data
values = [(None,"runny"),(None,"runnier"),(None,"runniest")]
cursor.executemany("INSERT INTO Runs VALUES (?,?)", values)
conn.commit()