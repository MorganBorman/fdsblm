import sys
import socket

class MumbleTeamConnection(object):
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.connect()
        
    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.hostname, self.port))
            sys.stderr.write("Established connection to mumble teams daemon.\n")
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
                sys.stderr.write("Failed to send message to mumble autoteam server. trying again...\n")
                sys.stderr.write("Reconnecting...\n")
                self.connect()
                    
            tries += 1
            
        sys.stderr.write("Failed to send message to mumble autoteam server. Could not succeed in 3 tries.\n")
    
    def changeteam(self, uid, server_name, team_name):
        self.send("changeteam {} {} {}\n".format(uid, server_name, team_name))
