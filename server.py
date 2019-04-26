import socket
import sys
import struct
import pymysql
import tree

#from apyori import apriori
import numpy as np
import pandas as pd
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score 
# from sklearn.metrics import classification_report 
# from sklearn.metrics import confusion_matrix 

client = None
cleaned_data = None

BUF_SIZE = 256

class MysqlHelper:
    def __init__(self, host = 'localhost', user = 'root', password = 'root', database = 'lahman2016', charset = 'utf8'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.db = None
        self.curs = None

    # connect
    def open(self):
        self.db = ps.connect(host=self.host, user=self.user, password=self.password,database=self.database, charset=self.charset)
        self.curs = self.db.cursor()

    # connect close
    def close(self):
        self.curs.close()
        self.db.close()

    # modify
    def cud(self, sql):
        self.open()
        try:
            rowCount = self.curs.execute(sql)
            if(rowCount > 0):
                client.send("Effected Row:".format{rowCount})
            self.close()
        except ps.MySQLError as e:
            client.send("Modification Error. Code:{0} Detail:{1}".format(e.args[0],e.args[1]))
            self.close()
        
    # search
    def find(self, sql):
        self.open()
        try:
            rowCount = self.curs.execute(sql)
            if(rowCount > 0):
                results = self.curs.fetchall()
            self.close()
            return results
        except ps.MySQLError as e:
            client.send("Query Error. Code:{0} Detail:{1}".format(e.args[0],e.args[1]))
            self.close()
            return e
        

    def consist_check(self,firstTable,secondTable,idName):
        #sql = "DELETE {0} FROM {0} INNER JOIN (SELECT {0}.{2} FROM {0} LEFT JOIN {1} ON {0}.{2} = {1}.{2} WHERE {1}.{2} IS NULL) as tmp on {0}.{2} = tmp.{2}".format(firstTable,secondTable,idName)
        sql = "SELECT {0}.{2} FROM {0} LEFT JOIN {1} ON {0}.{2} = {1}.{2} WHERE {1}.{2} IS NULL".format(firstTable,secondTable,idName)
        results = self.find(sql)
        if(len(results) > 0):
            client.send('There are {0} entries that exist in {1} but not in {2} for {3}. Please reply 1 to delete or complete SQL query to Adjust it'.format(len(results),firstTable,secondTable,idName))
            reply = client.recv(16384)
            if(reply == '1'):
                sql = "DELETE {0} FROM {0} INNER JOIN (SELECT {0}.{2} FROM {0} LEFT JOIN {1} ON {0}.{2} = {1}.{2} WHERE {1}.{2} IS NULL) as tmp on {0}.{2} = tmp.{2}".format(firstTable,secondTable,idName)
                self.cud(sql)
            else:
                sql = client.recv(16384)
                #sql = UPDATE HallOfFame SET playerID='drewjd01' WHERE playerID='drewj.01'
                self.cud(sql)


    def add_index(self,table,indexName):
        sql = "ALTER TABLE {0} ADD INDEX ({1});".format(table,indexName)
        results = self.cud(sql)
        return results
 
 
def start_tcp_server(ip, port):
    # create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (ip, port)

    # Set Timeout to 60 sec
    s.settimeout(60)
 
    # bind port
    print("starting listen on ip %s, port %s" % server_address)
    sock.bind(server_address)
 
    # set a new buffer size
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, BUF_SIZE)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUF_SIZE)

    # start listening, allow only one connection
    try:
        sock.listen(1)
    except socket.error as e:
        print("fail to listen on port %s" % e)
        sys.exit(1)
    
    print("waiting for connection")
    client, addr = sock.accept()
    print("having a connection")
        
    msg = 'welcome to tcp server' + "\r\n"

    while True:
        msg = client.recv(16384)
        msg_de = msg
        
        if msg_de == '4':
            print("Client Requested to Disconnect, Disconnecting...")
            break
        ##############################################
        #Run Procedure HERE
        elif msg_de == '1':
            if(client.recv(16384) == 'Y')
                commit = True
                role = client.recv(16384)
                period = client.recv(16384)
                clean(commit,role,period)
            else:
                role = client.recv(16384)
                period = client.recv(16384)
        elif msg_de == '2':
            analyze()
        elif msg_de == '3':
            validate()
        else:
            client.send('unknown option')


        ##############################################
 
        client.send(msg)
 
    client.close()
    sock.close() 
    print("Disconnected")

def clean(commit = False):
    mh = MysqlHelper('localhost', 'root', 'root', 'lahman2016', 'utf8')

    #########################################################
    #Default Cleanup Process
    results = mh.add_index('Master','playerID')
    results = mh.add_index('Batting','playerID')
    results = mh.add_index('Pitching','playerID')
    results = mh.add_index('Fielding','playerID')
    results = mh.add_index('AllstarFull','playerID')
    results = mh.add_index('HallOfFame','playerID')
    results = mh.add_index('Managers','playerID')

    results = mh.add_index('Batting','yearID')
    results = mh.add_index('Pitching','yearID')
    results = mh.add_index('Fielding','yearID')
    results = mh.add_index('AllstarFull','yearID')
    results = mh.add_index('Managers','yearID')
    results = mh.add_index('HallOfFame','yearID')

    results = mh.consist_check('Batting','Master','playerID')
    results = mh.consist_check('Pitching','Master','playerID')
    results = mh.consist_check('Fielding','Master','playerID')
    results = mh.consist_check('HallOfFame','Master','playerID')

    
    sql = "DELETE FROM Master WHERE finalGame = '' OR debut = ''"
    results = mh.cud(sql)
    # if a player is not inducted and vote is less than 5%, he is out of the pool
    sql = "DELETE FROM HallOfFame WHERE inducted = 'N' AND votes/ballots < 0.05"
    results = mh.cud(sql)
    #since player is not eligible if not retired for at least 5 years or they do not meet ten year rule
    sql = "DELETE FROM Master WHERE finalGame > '2011-12-31' or LEFT(finalGame,4)-LEFT(debut,4) < 10;"
    results = mh.cud(sql)
    sql = "DELETE t1 FROM HallOfFame t1, HallOfFame t2 WHERE t1.inducted < t2.inducted and t1.playerID = t2.playerID;"
    results = mh.cud(sql)

    ################################################

    #identify forms of consistency and sanity checking
    #determine if there are problems with portions of data using query
    #implement solution such as ignore and create new table for analysis, or adjusting analysis in order to compensate for data skew(long tail of data distribution)
    #parameter should include threshold and identified by client

    # playerID,Career Win, Career ShoutOut, Career StrikeOut,Career Hits,Career HomeRun,Career RBI (Runs Batted In), Career OBP(On base percentage), Career All Star Appearence
    sql = 'SELECT playerID,ifnull(tot_W,0) as tot_W,ifnull(tot_SHO,0)as tot_SHO,ifnull(tot_SO,0) as total_SO,tot_H,tot_HR,tot_RBI,ifnull(OBP,0) as total_OBP,ifnull(ASA,0)as ASA from ((Select playerID, sum(W) as tot_W, sum(SHO) as tot_SHO, sum(SO) as tot_SO from Pitching group by (playerID))as t1 right join (select playerID,sum(H) as tot_H,sum(HR) as tot_HR, sum(RBI) as tot_RBI, sum(H+BB+HBP)/sum(AB+BB+SF+HBP) as OBP from Batting group by (playerID))as t2 using (playerID) left join (select playerID,sum(GP) as asa from AllstarFull group by (playerID)) as t3 using (playerID));'

        # Select playerID,tot_W,tot_SHO,tot_SO,tot_H,tot_RBI,OBP,ASA from ((Select playerID,sum(W) as tot_W,sum(SHO) as tot_SHO,sum(SO) as tot_SO from Pitching group by (playerID)) inner join (select playerID,sum(H) as tot_H,sum(RBI) as tot_RBI sum(H+BB+HBP)/sum(AB+BB+SF+HBP) as OBP from Batting group by (playerID)) using (playerID) inner join (select playerID,sum(GP) as asa from AllstarFull group by (playerID)) using (playerID);
    cleaned_data = mh.find(sql)

    if commit: # not as expected 
        mh.db.commit()
    else:
        mh.db.rollback()



# Predict who will be inducted into Hall of Fame
def analyze(category,period):
    detree = DecisionTreeClass()
    detree.fit(cleaned_data,result)
    # Stats to be considered: Wins(W),Losses(L),Strike-out(SO),Hits(H),Homer(HR),All Start Appearence count,
    # Minimized return to Client, only the result
    

def validate():
    #divide data into two at random.
    #first half would be used to analysis and predict for the oter half
    #The other half would be used to validate or refute hypothesis
    #return should be validated or not, probably with some reason
    print("TODO")


 
 
 
if __name__=='__main__':
    communication = Process(start_tcp_server('127.0.0.1',6000))
    p1.start()
    p1.join()