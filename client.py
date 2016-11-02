#---Get a file from socket connection---#

#using socket library for connections
import socket

#initialize socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#set host to ip of pi, if on same network use
#local ip
host = '192.168.1.26'

#open port to use, must be same as port
#server on pi is using
port = 9005

#Attempt to connect to server on pi
s.connect((host, port))

#create file
#name of file, write binary
newFile = open('server2.py', 'wb')

#recieve data, only 1024 bytes
data = s.recv(1024)

#loop to get all data
i = 0
while(i < 10):
  #write binary to file
  newFile.write(data)
  #recieve file
  data = s.recv(1024)
  i+=1

#close file
newFile.close()

#close socket connection
s.close()
