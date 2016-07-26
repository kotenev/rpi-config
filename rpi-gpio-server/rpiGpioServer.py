#!/usr/bin/env jython

import rpiGpioInterface.py as Interface
import rpiGpioParser.py as Parser
import socket
import sys

def socketSetup():
    HOST = None # Symbolic name meaning all available interfaces 
    PORT = 50007 # Arbitrary non-privileged port 
    s = None 
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
    
        af, socktype, proto, canonname, sa = res 
        
        try:
            s = socket.socket(af, socktype, proto)
    
        except socket.error, msg:
            s = None 
            continue
    
        try:
            s.bind(sa) 
            s.listen(1)
            
        except socket.error, msg:
            s.close() 
            s = None 
            continue
    
        break
    
    if s is None:
        print ("could not open socket") 
        sys.exit(1)
        
    return s

gpio = Interface.Interface()
parser = Parser.Parser(gpio)

sock = socketSetup()
while True:
    conn, addr = sock.accept() 
    print ("Connected by", addr) 
    while True:
        data = conn.recv(1024) 
        if not data: 
            break 
        data = parser.parse(data)
        conn.send(data)
    
    conn.close()
