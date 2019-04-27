import socket
import sys
import struct
import pymysql as ps
import tree

import numpy as np
import pandas as pd

client = None
feature_list = None
result_list = None
validate_list = None
vali_res_list = None

BUF_SIZE = 256

class MysqlHelper:
    def __init__(self, host = 'localhost', user = 'root', password = '940326', database = 'lahman2016', charset = 'utf8'):
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
    def cud(self, sql,client):
        self.open()
        try:
            rowCount = self.curs.execute(sql)
            print(rowCount)
            if(rowCount > 0):
                client.send("Effected Row:{0}".format(rowCount).encode())
        except ps.MySQLError as e:
            client.send("Modification Error. Code:{0} Detail:{1}".format(e.args[0],e.args[1]).encode())
        finally:
            self.close()
        
    # search
    def find(self, sql,client):
        self.open()
        try:
            results = ()
            rowCount = self.curs.execute(sql)
            if(rowCount > 0):
                results = self.curs.fetchall()
        except ps.MySQLError as e:
            print("Query Error. Code:{0} Detail:{1}".format(e.args[0],e.args[1]))
            client.send("Query Error. Code:{0} Detail:{1}".format(e.args[0],e.args[1]).encode())
            raise
        except ps.InterfaceError as ie:
            print("Interface Error. Code:{0} Detail:{1}".format(e.args[0],e.args[1]))
            raise
        finally:
            self.close()
            return results
        
    # Consistency Check
    def consist_check(self,client,firstTable,secondTable,idName):
        print("Running Consistency Check {0} {1} {2}...".format(firstTable,secondTable,idName))
        sql = "SELECT {0}.{2} FROM {0} LEFT JOIN {1} ON {0}.{2} = {1}.{2} WHERE {1}.{2} IS NULL".format(firstTable,secondTable,idName)
        results = self.find(sql,client)
        if(len(results) > 0):
            client.send('O:There are {0} entries that exist in {1} but not in {2} for {3}. Please reply 1 to delete or anything to bypass it'.format(len(results),firstTable,secondTable,idName).encode())
            reply = None
            while(reply == None):
                reply = client.recv(16384).decode()
            print(reply)
            if(reply == '1'):
                sql = "DELETE {0} FROM {0} INNER JOIN (SELECT {0}.{2} FROM {0} LEFT JOIN {1} ON {0}.{2} = {1}.{2} WHERE {1}.{2} IS NULL) as tmp on {0}.{2} = tmp.{2}".format(firstTable,secondTable,idName)
                self.cud(sql,client)
        print("Finished Consistency Check {0} {1} {2}".format(firstTable,secondTable,idName))                

    # Adding Index
    def add_index(self,client,table,indexName):
        print("Adding Index {0}".format(table))
        sql = "ALTER TABLE {0} ADD INDEX ({1});".format(table,indexName)
        results = self.cud(sql,client)
        return results

    # Revert databse
    def revertdb(self,stmts):
        self.open()
        for sql in stmts:
            self.curs.execute(sql)
        self.close()
 
 
def start_tcp_server(ip, port):
    # create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (ip, port)

    # Set Timeout to 60 sec
    sock.settimeout(30)
 
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
    print("Connected")
    try:
        while True:
            period = None
            msg = client.recv(16384)
            msg_de = msg.decode()
            print(msg_de)
            
            if msg_de == '4':
                print("Client Requested to Disconnect, Disconnecting...")
                break
            ##############################################
            #Run Procedure HERE
            elif msg_de == '1':
                if(client.recv(16384) == 'Y'):
                    commit = True
                    while(period == None):
                        period = client.recv(16384).decode()
                    clean(client,commit,period)
                else:
                    while(period == None):
                        period = client.recv(16384).decode()
                    clean(client)
            elif msg_de == '2':
                analyze(client)
            elif msg_de == '3':
                validate(client)
            elif msg_de == 'R':
                revert(client)
            else:
                client.send('unknown option'.encode())
                raise

            ##############################################
    except:
        print("EXCEPT EXIT")
        print(sys.exc_info()[0], sys.exc_info()[1])
    finally:
        client.send('4'.encode())
        client.close()
        sock.close() 
    print("Disconnected")

def clean(client,commit = False,period = 2010):
    global feature_list
    global result_list
    global validate_list 
    global vali_res_list 

    print('Start Cleaning...')
    mh = MysqlHelper()

    #########################################################
    # Default Cleanup Process
    results = mh.add_index(client,'Master','playerID')
    results = mh.add_index(client,'Batting','playerID')
    results = mh.add_index(client,'Pitching','playerID')
    results = mh.add_index(client,'Fielding','playerID')
    results = mh.add_index(client,'AllstarFull','playerID')
    results = mh.add_index(client,'HallOfFame','playerID')
    results = mh.add_index(client,'Managers','playerID')

    results = mh.add_index(client,'Batting','yearID')
    results = mh.add_index(client,'Pitching','yearID')
    results = mh.add_index(client,'Fielding','yearID')
    results = mh.add_index(client,'AllstarFull','yearID')
    results = mh.add_index(client,'Managers','yearID')
    results = mh.add_index(client,'HallOfFame','yearID')

    print('Finished Adding Index')

    #########################################################
    #Consistancy Check
    results = mh.consist_check(client,'Batting','Master','playerID')
    results = mh.consist_check(client,'Pitching','Master','playerID')
    results = mh.consist_check(client,'Fielding','Master','playerID')
    results = mh.consist_check(client,'HallOfFame','Master','playerID')

    print('Finished Consistancy Check')
    #########################################################
    # Sanity Check
    sql = "DELETE FROM Master WHERE finalGame = '' OR debut = ''"
    results = mh.cud(sql,client)
    # if a player is not inducted and vote is less than 5%, he is out of the pool
    sql = "DELETE FROM HallOfFame WHERE inducted = 'N' AND votes/ballots < 0.05"
    results = mh.cud(sql,client)
    sql = "UPDATE HallOfFame SET playerID='drewjd01' WHERE playerID='drewj.01'"
    results = mh.cud(sql,client)
    #since player is not eligible if not retired for at least 5 years or they do not meet ten year rule
    sql = "DELETE FROM Master WHERE finalGame > '2011-12-31' or LEFT(finalGame,4)-LEFT(debut,4) < 10;"
    results = mh.cud(sql,client)
    #Delete older record for player and keep only the latest
    sql = "DELETE t1 FROM HallOfFame t1, HallOfFame t2 WHERE t1.yearid < t2.yearid and t1.playerID = t2.playerID;"
    results = mh.cud(sql,client)
    print('Finished Sanity Check')
    ##########################################################

    #implement solution such as ignore and create new table for analysis, or adjusting analysis in order to compensate for data skew(long tail of data distribution)

    # Get Train Set
    # playerID,Career Win, Career ShoutOut, Career StrikeOut,Career Hits,Career HomeRun,Career RBI (Runs Batted In), Career OBP(On base percentage), Career All Star Appearence, lastyear
    sql = 'DROP VIEW IF EXISTS TrainSet;'
    results = mh.cud(sql,client)
    sql = 'CREATE VIEW TrainSet AS SELECT playerID, IFNULL(tot_W, 0) AS tot_W, IFNULL(tot_SHO, 0) AS tot_SHO,IFNULL(tot_SO, 0) AS total_SO,tot_H,tot_HR,tot_RBI,IFNULL(OBP, 0) AS total_OBP,IFNULL(ASA, 0) AS ASA,lastYear FROM((SELECT playerID, SUM(W) AS tot_W, SUM(SHO) AS tot_SHO, SUM(SO) AS tot_SO FROM Pitching GROUP BY (playerID)) AS t1 RIGHT JOIN (SELECT playerID, SUM(H) AS tot_H, SUM(HR) AS tot_HR, SUM(RBI) AS tot_RBI, SUM(H + BB + HBP) / SUM(AB + BB + SF + HBP) AS OBP FROM Batting GROUP BY (playerID)) AS t2 USING (playerID) LEFT JOIN (SELECT playerID, SUM(GP) AS asa FROM AllstarFull GROUP BY (playerID)) AS t3 USING (playerID) LEFT JOIN (SELECT playerID, LEFT(finalGame, 4) AS lastYear FROM Master) AS t4 USING (playerID));'
    results = mh.cud(sql,client)

    sql = 'SELECT * FROM TrainSet where lastYear < {0} ORDER BY playerID ASC;'.format(period)
    feature_list = mh.find(sql,client)

    sql = "SELECT Distinct(playerID),if(inducted = 'Y',1,0) AS inducted FROM TrainSet Left JOIN (SELECT playerID,inducted FROM HallOfFame) as tmp USING (playerID) WHERE lastYear < {0} ORDER BY playerID;".format(period)
    result_list = mh.find(sql,client)

    print(len(feature_list))
    print(len(result_list))
    mh.open()
    if commit: # not as expected 
        mh.db.commit()
    else:
        mh.db.rollback()
    mh.close()

    print("Finished Cleanup")
    client.send("Finished".encode())

# Predict who will be inducted into Hall of Fame
def analyze(client):
    global feature_list
    global result_list
    if(feature_list == None or result_list == None):
        client.send("data is not cleaned yet, please clean data first".encode())
        return

    #TODO: Convert result_list to 1D

    detree = tree.DecisionTreeClass()
    detree.fit(feature_list[:len(result_list+1)],result_list)
    # Stats to be considered: Wins(W),Losses(L),Strike-out(SO),Hits(H),Homer(HR),All Start Appearence count,
    # Minimized return to Client, only the result
    client.send("Finished".encode())

def validate(client):
    global validate_list 
    global vali_res_list 
    #divide data into two at random.
    #first half would be used to analysis and predict for the other half
    #The other half would be used to validate or refute hypothesis
    #return should be validated or not, probably with some reason
    
    client.send("Finished".encode())

def revert(client):
    mh = MysqlHelper()
    original_sql = open("lahman2016.sql", 'r').readlines()
    stmts = []
    DELIMITER = ';'
    stmt = ''

    for ln, line in enumerate(original_sql):
        if line.startswith('--'):
            continue

        if not line.strip():
            continue

        if (DELIMITER not in line):
            stmt += line.replace(DELIMITER, ';')
            continue

        if stmt:
            stmt += line
            stmts.append(stmt.strip())
            stmt = ''
        else:
            stmts.append(line.strip())

    mh.revertdb(stmts)
    return
 
if __name__=='__main__':
        start_tcp_server('127.0.0.1',6000)


