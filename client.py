import socket
import sys
import time
 
import pymysql as ps	
			
isClean = False
isAnalyzed = False

def start_tcp_client(ip, port): 
	###create socket
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# Set Timeout to 60 sec
	#server.settimeout(60)

	failed_count = 0
	while True:
		try:
			print("start connect to server ")
			server.connect((ip, port))
			break
		except socket.error:
			failed_count += 1
			time.sleep(5)
			print("fail to connect to server %d times" % failed_count)
			if failed_count == 10: return

	quit = False
	# send and receive
	while (not quit):
		create_menu()
		tmp = input()
		if tmp == '1':
			if(clean(server) == '4'):
				quit = True
		elif tmp == '2':
			analyze(server)
		elif tmp == '3':
			validate(server)
		elif (tmp == 'R' or tmp == 'r'):
			revert(server)
		elif (tmp == '4' or rec == '4'):
			server.send('4'.encode())
			quit = True
		else:
			print("Invalid Option, Please enter your option again")
			#print("You should not be here, Report the detail how you reach this line to my lovely cat")
		if(quit):
			break
	server.close()

#Clean Data
#Parameter includes database name, table name,all the parameter required...
def clean(s):
	global isClean
	s.send('1'.encode())
	print("Please Enter the Option:")
	print("Do you want to commit the change? (Y/N)")
	tmp = input()
	if(tmp == 'y' or tmp == 'Y'):
		s.send('Y'.encode())
	else:
		s.send('N'.encode())
	isClean = False
	while(not isClean):
		tmp = s.recv(1024).decode()
		if(tmp == "Finished"):
			isClean = True
			print('Data Cleaned')
		elif(tmp == '4'):
			return tmp
		elif(tmp != ''):
			print(tmp)
			if(tmp[0] == 'O'):
				tmp = input()
				s.send(tmp.encode())
	return

#Analyze data
def analyze(s):
	global isClean
	if(not isClean):
		print("Data is not cleaned, default clean has started...")
		clean()
	s.send('2'.encode())
	#Check if data is cleaned

#Validate analysis
def validate(s):
	if(not isAnalyzed):
		print("Data is not analyzed, default clean has started...")
		analyze()
	s.send('3'.encode())
	#Check if data is analyzed

def revert(s):
	s.send('R'.encode())


def create_menu():
	print("1: Data Clean")
	print("2: Data Analyze")
	print("3: Data Validate")
	print("R: Revert Database")
	print("4: Quit")

if __name__=='__main__':
	start_tcp_client('127.0.0.1',6000)
