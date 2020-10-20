import sqlite3 as sql
from os.path import expanduser
from pathlib import Path
import datetime as dt

#ToDo
#decide where events should take place (M_C? managers?)
#decide whether to use RxPy3 for events
#implement emulator modes

home = expanduser('~')
savedir = home + '/SIEData/'

class RunDBRecorder:
    def __init__(self,dbname='test.db'):
        self.dbpath = savedir + dbname
        self.activeRunId = 0
       
    def CreateNewRun(self, runName=None):
        conn = sql.connect(self.dbpath)
        cursor = conn.cursor()
        #generate runName based on number of today's runs
        if(not runName):
            cursor.execute('''SELECT Count() FROM Runs
            WHERE run_date IS ?;''',[dt.date.today()])
            rows = cursor.fetchone()[0]
            print('number of rows: ' + str(rows))
            now = dt.datetime.now()
            runName = now.strftime('%Y%m%d') + '_' + str(rows)
            print('runName: ' + runName)

if __name__ == '__main__':  
    rec = RunDBRecorder()
    rec.CreateNewRun()