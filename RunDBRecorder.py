import sqlite3 as sql
from os.path import expanduser
from pathlib import Path
import datetime as dt
import random
import time

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
        self.isRecording = False
        self.startTime = time.clock()

    def ElapsedTime(self):
        return round((time.clock() - self.startTime),3)
       
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
            runName = now.strftime('%Y%m%d') + '_' + str(rows+1)
            print('runName: ' + runName)
        values = (None,runName,dt.date.today())
        cursor.execute('INSERT INTO Runs VALUES (?,?,?)',values)
        conn.commit()
        #this is bad practice and we should fetch run_id directly (but presently I'm too lazy)
        self.activeRunId = rows + 1

    def AddCommandData(self, runId=None, time = None, cnc=None, ra=None, syr=None):
        if not runId:
            runId = self.activeRunId
        if not time:
            time = self.ElapsedTime()
        print('runId: ' + str(runId))
        conn = sql.connect(self.dbpath)
        cursor = conn.cursor()
        values = (None,time,cnc,ra,syr,runId)
        cursor.execute('INSERT INTO Commands VALUES (?,?,?,?,?,?)',values)
        conn.commit()

    def StartRun(self, runId=None, isFresh = True):
        print('RecorededRun()')
        if isFresh:
            self.CreateNewRun()
        self.startTime = time.clock()
        #while(self.isRecording):
            #is it necessary to do anything?

    def StopRun(self):
        if self.isRecording:
            self.isRecording = False
        

def RandomStr():
    MAX_LIMIT = 111    
    random_string = ''    
    for _ in range(10):
        random_integer = random.randint(101, MAX_LIMIT)
        # Keep appending random characters using chr(x)
        random_string += (chr(random_integer))    
    print('random_string: ' + random_string)
    return random_string

if __name__ == '__main__':  
    rec = RunDBRecorder()
    rec.CreateNewRun()
    i=1111
    while(i>0):
        rec.AddCommandData(
            cnc=RandomStr(),
            ra=RandomStr(),
            syr=RandomStr()
            )
        i-=1