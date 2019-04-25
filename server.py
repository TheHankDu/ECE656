import socket
import sys
import struct
import pymysql

#from apyori import apriori
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
 
 
SEND_BUF_SIZE = 256
 
RECV_BUF_SIZE = 256
 
Communication_Count: int = 0
 
receive_count : int = 0

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
            self.curs.execute(sql)
        except:
            print('modify error')
        self.close()

    # search
    def find(self, sql, params):
        self.open()
        try:
            result = self.curs.execute(sql, params)
            self.close()
            results = self.curs.fetchall()
            return results
        except ProgrammingError as e:
            print('find error')
            return 1
        except MySQLError as e:
            return e.args[0]

    def consist_check(self,firstTable,secondTable,idName):
        sql = "DELETE {0} FROM {0} INNER JOIN (SELECT {0}.{2} FROM {0} LEFT JOIN {1} ON {0}.{2} = {1}.{2} WHERE {1}.{2} IS NULL) as tmp on {0}.{2} = tmp.{2}".format(firstTable,secondTable,idName)
        results = self.cud(sql)
        return results

    def add_index(self,table,indexName):
        sql = "ALTER TABLE {0} ADD INDEX ({1});".format(table,indexName)
        results = self.cud(sql)
        return results
 
 
def start_tcp_server(ip, port):
    # create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (ip, port)
 
    # bind port
    print("starting listen on ip %s, port %s" % server_address)
    sock.bind(server_address)
 
    # get the old receive and send buffer size
    s_send_buffer_size = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    s_recv_buffer_size = sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
    print("socket send buffer size[old] is %d" % s_send_buffer_size)
    print("socket receive buffer size[old] is %d" % s_recv_buffer_size)
 
    # set a new buffer size
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, SEND_BUF_SIZE)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, RECV_BUF_SIZE)
 
    # get the new buffer size
    s_send_buffer_size = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    s_recv_buffer_size = sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
    print("socket send buffer size[new] is %d" % s_send_buffer_size)
    print("socket receive buffer size[new] is %d" % s_recv_buffer_size)
 
    # start listening, allow only one connection
    try:
        sock.listen(1)
    except socket.error as e:
        print("fail to listen on port %s" % e)
        sys.exit(1)
    while True:
        print("waiting for connection")
        client, addr = sock.accept()
        print("having a connection")
        break
    msg = 'welcome to tcp server' + "\r\n"
    receive_count = 0
    receive_count += 1
    while True:
        print("\r\n")
        msg = client.recv(16384)
        msg_de = msg.decode('utf-8')
        
        if msg_de == '4':
            print("Client Requested to Disconnect, Disconnecting...")
            break
 
        client.send(msg.encode('utf-8'))
 
    client.close()
    sock.close() 
    print("Disconnected")

def clean(commit = False,role,period):
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

    results = mh.consist_check('user_elite','Batting','yearID')
    results = mh.consist_check('user_friends','user','yearID')
    results = mh.consist_check('tip','user','yearID')
    results = mh.consist_check('review','user','yearID')

    
    sql = "DELETE FROM Master WHERE birthYear == ''"
    results = mh.cud(sql)
    sql = "DELETE FROM HallOfFame WHERE inducted = 'N'"
    results = mh.cud(sql)
    #since player is not eligible if not retired for at least 5 years or they do not meet ten year rule
    sql = "DELETE FROM Master WHERE finalGame > '2011-12-31' OR finalGame-debut<10"


    sql = 'select * FROM HallOfFame where not exists (select playerID from Master where playerID = HallOfFame.playerID);'
    results = mh.cud(sql)
    if(results != emptyset):
        #ask user for the choices: delete or update
        #if delete
            #sql = "DELETE FROM {0} WHERE playerID = {0}".format('HallOfFame',results)
        #elif update
            #sql = UPDATE HallOfFame SET playerID='drewjd01' WHERE playerID='drewj.01';


    ################################################

    #identify forms of consistency and sanity checking
    #determine if there are problems with portions of data using query
    #implement solution such as ignore and create new table for analysis, or adjusting analysis in order to compensate for data skew(long tail of data distribution)
    #parameter should include threshold and identified by client

    if commit: # not as expected 
        mh.db.commit()
    else:
        mh.db.rollback()



# Predict who will be inducted into Hall of Fame
def analyze():
    print("TODO")

    # Minimized return to Client, only the result
    

def validate(playerID ):
    #divide data into two at random.
    #first half would be used to analysis and predict for the oter half
    #The other half would be used to validate or refute hypothesis
    #return should be validated or not, probably with some reason
    print("TODO")


 
 
 
if __name__=='__main__':
    communication = Process(start_tcp_server('127.0.0.1',6000))
    p1.start()