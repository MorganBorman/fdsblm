import sys
import struct
import socket

def ip_to_string(iplong):
    return socket.inet_ntoa(struct.pack('<L', iplong))

class IrcBotConnection(object):
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.connect()
        
    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.hostname, self.port))
            sys.stderr.write("Established connection to irc bot daemon.\n")
        except socket.error:
            pass
    
    def send(self, msg):
        tries = 0
        while tries < 3:
            try:
                result = self.socket.sendall(msg)
                if result is None:
                    sys.stderr.write("Successfully sent message: {}\n".format(repr(msg)))
                    return
            except socket.error:
                sys.stderr.write("Failed to send message to irc bot. trying again...\n")
                sys.stderr.write("Reconnecting...\n")
                self.connect()
                    
            tries += 1
            
        sys.stderr.write("Failed to send message to irc bot. Could not succeed in 3 tries.\n")
    
    def complaint(self, server_name, complainer_ip, complainer_name, complainee_ip, complainee_name, issue):
        complainer_ip = ip_to_string(complainer_ip)
        complainee_ip = ip_to_string(complainee_ip)
        
        self.send("{}: {}({}) reports {}({}) for '{}'\n".format(server_name, complainer_name, complainer_ip, complainee_name, complainee_ip, issue))
