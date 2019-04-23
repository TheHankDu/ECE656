import socket
import sys
import struct
import pymysql

from apyori import apriori
import numpy as np
import pandas as pd
 
 
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
    def cud(self, sql, params):
        self.open()
        try:
            self.curs.execute(sql, params)
            self.db.commit()
            print("ok")
        except:
            print('modify error')
            self.db.rollback()
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
        print("recv len is : [%d]" % len(msg_de))
        print("###############################")
        print(msg_de)
        print("###############################")
        
        if msg_de == 'disconnect':break
 
        msg = ("hello, client, i got your msg %d times, now i will send back to you " % receive_count)
        client.send(msg.encode('utf-8'))
        receive_count += 1
        print("send len is : [%d]" % len(msg))
 
    print("finish test, close connect")
    client.close()
    sock.close() 
    print(" close client connect ")

def consist_check(mh,firstTable,secondTable,idName):
    sql = "DELETE {0} FROM {0} INNER JOIN (SELECT {0}.{2} FROM {0} LEFT JOIN {1} ON {0}.{2} = {1}.{2} WHERE {1}.{2} IS NULL) as tmp on {0}.{2} = tmp.{2}".format(firstTable,secondTable,idName)
    results = mh.cud(sql)
    return results

def add_index(mh,table,indexName):
    sql = "ALTER TABLE {0} ADD INDEX ({1});".format(table,indexName)
    results = mh.cud(sql)
    return results


def revert():
    #Revert from backup table

def clean(table='',attr='',condition,sql = '',consistency = True,commit = False):
    # 1. Create New Table called temp to store all the change 
    # 2. Peroform Data Clean
    # 3. Commit change and update table if success
    # 4. Delete temp if failed
    
    mh = MysqlHelper('localhost', 'root', 'root', 'lahman2016', 'utf8')

    if(sql):
        result = mh.cud(sql)
        return
    else:
        #do following

    #########################################################
    #Default Cleanup Process
    results = add_index(mh,Master,playerID)
    results = add_index(mh,Batting,playerID)
    results = add_index(mh,Pitching,playerID)
    results = add_index(mh,Fielding,playerID)
    results = add_index(mh,AllstarFull,playerID)
    results = add_index(mh,HallOfFame,playerID)
    results = add_index(mh,Managers,playerID)
    results = add_index(mh,FieldingOF,playerID)
    results = add_index(mh,BattingPost,playerID)
    results = add_index(mh,PitchingPost,playerID)
    results = add_index(mh,ManagersHalf,playerID)
    results = add_index(mh,Salaries,playerID)
    results = add_index(mh,AwardsManagers,playerID)
    results = add_index(mh,AwardsPlayers,playerID)
    results = add_index(mh,AwardsShareManagers,playerID)
    results = add_index(mh,AwardsSharePlayers,playerID)
    results = add_index(mh,FieldingPost,playerID)
    results = add_index(mh,Appearances,playerID)
    results = add_index(mh,CollegePlaying,playerID)
    results = add_index(mh,FieldingOFsplit,playerID)




    results = consist_check('business_categories','business','business_id')
    results = consist_check('checkin','business','business_id')
    results = consist_check('review','business','business_id')
    results = consist_check('tip','business','business_id')

    sql = "ALTER TABLE user ADD INDEX (user_id);"
    mh.cud(sql)
    sql = "ALTER TABLE user_elite ADD INDEX (user_id);"
    mh.cud(sql)
    sql = "ALTER TABLE user_friends ADD INDEX (user_id);"
    mh.cud(sql)
    sql = "ALTER TABLE tip ADD INDEX (user_id);"
    mh.cud(sql)
    sql = "ALTER TABLE review ADD INDEX (user_id);"
    mh.cud(sql)

    results = consist_check('user_elite','user','user_id')
    results = consist_check('user_friends','user','user_id')
    results = consist_check('tip','user','user_id')
    results = consist_check('review','user','user_id')

    
    sql = "DELETE FROM user_elite WHERE year < 2004 OR year > 2019"
    results = mh.cud(sql)
    sql = "DELETE FROM review WHERE date < '2004-09-30' OR date > '2019-04-27'"
    results = mh.cud(sql)
    sql = "DELETE FROM tip WHERE date < '2004-09-30' OR date > '2019-04-27'"
    results = mh.cud(sql)
    sql = "DELETE FROM user WHERE yelping_since < '2004-09-30' OR yelping_since > '2019-04-27'"
    ################################################

    #identify forms of consistency and sanity checking
    #determine if there are problems with portions of data using query
    #implement solution such as ignore and create new table for analysis, or adjusting analysis in order to compensate for data skew(long tail of data distribution)
    #parameter should include threshold and identified by client
    if(table && attr && condition):
        sql = 'SELECT * FROM {0} WHERE {1} {2}'.format(table,attr,condition)
        results = mh.find(sql)
        #check if results is error, if yes, ask client for choices


    if commit: # not as expected 
        mh.db.commit()
    else:
        mh.db.rollback()



#Analyze Data include detailed and careful study of particular things 
def analyze():
    # a priori algorithm for operation hours on the rating of business
    # joining business,business_categories

    # Minimized return to Client, only the result
    

def validate():
    #divide data into two at random.
    #first half would be used to analysis and predict for the oter half
    #The other half would be used to validate or refute hypothesis
    #return should be validated or not, probably with some reason
    print("TODO")


 
 
 
if __name__=='__main__':
    start_tcp_server('127.0.0.1',6000)