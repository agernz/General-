#---Transfer a file over socket connection---#

#using socket library for connections
import socket

#initialize socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#0.0.0.0 uses all available ip addresses, wifi, ethernet etc
host = '0.0.0.0'

#open port to use for pi, *use same port for client
port = 9005

#A socket is like a gateway made up of an ip and
#port number, this statement creates the socket
#with the defined ip and port number
s.bind((host, port))

#allow up to 1 clients to connect
s.listen(1)

#flag to tell program when to end
running = True

#keep checking for a connection from a
#client
while running:

  #accept returns the client and address of client
  c, addr = s.accept()
  
  #a client has connected, can exit program
  if addr != None:
    running = False

  #display client's address
  print ('Got connection from',addr)

  #send client a file
  #open a file, read binary
  readByte = open('server.py', 'rb')
  data = readByte.read()
  #close file
  readByte.close()

  #send binary file
  c.send(data)

  #end connection with client
  c.close()

print('clean exit')
