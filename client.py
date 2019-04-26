import socket
import sys
import time
 
receive_count = 0
import pymysql as ps	
			
s = None
isClean = False
isAnalyzed = False

def start_tcp_client(ip, port): 
	###create socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# Set Timeout to 60 sec
	s.settimeout(60)

	failed_count = 0
	while True:
		try:
			print("start connect to server ")
			s.connect((ip, port))
			break
		except socket.error:
			failed_count += 1
			time.sleep(5)
			print("fail to connect to server %d times" % failed_count)
			if failed_count == 10: return

	# send and receive
	#get the socket send buffer size and receive buffer size
	s_send_buffer_size = s.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
	s_receive_buffer_size = s.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)

	while True:
		quit = create_menu()
		if(quit):
			break
		print("Waiting for Server Response...")
		rec = s.recv(1024).decode()
		print(rec)
	s.close()

#Clean Data
#Parameter includes database name, table name,all the parameter required...
def clean():
	s.send('1'.encode())
	print("Please Enter the Option:")
	print("Do you want to commit the change? (Y/N)")
	tmp = input()
	if(tmp == 'y' or tmp == 'Y'):
		s.send('Y'.encode())
	else:
		s.send('N'.encode())
	
	while(!isClean):
		tmp = s.recv(1024).decode()
		if(tmp = "Finished"):
			isClean = True
		print(tmp)
	return

#Analyze data
def analyze():
	if(!isClean):
		print("Data is not cleaned, default clean has started...")
		clean()
	s.send('2'.encode())
	#Check if data is cleaned

#Validate analysis
def validate():
	s.send('3'.encode())
	#Check if data is analyzed


def create_menu():
	quit = False
	print("1: Data Clean")
	print("2: Data Analyze")
	print("3: Data Validate")
	print("4: Quit")
	tmp = input()
	if tmp == '1':
		clean()
	elif tmp == '2':
		analyze()
	elif tmp == '3':
		validate()
	elif tmp == '4':
		quit = True
	else:
		print("Invalid Option, Please enter your option again")
		#print("You should not be here, Report the detail how you reach this line to my lovely cat")
	return quit

if __name__=='__main__':
	start_tcp_client('127.0.0.1',6000)
