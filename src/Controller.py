from AuthenticationModel import AuthenticationModel
from ServersModel import ServersModel
from SocketManager import SocketManager

from BaseTables import IpName

import time, datetime

def cs_escape(string):
    """Replace any double quotes with single quotes."""
    return string.replace('\"', "''")

def format_date(epoch_seconds):
    date = datetime.datetime.fromtimestamp(epoch_seconds)
    
    now = time.time()
    
    if now-epoch_seconds > (60*60*24*2):
        return date.strftime("%Y/%m/%d")
    elif now-epoch_seconds > (60*60*24):
        return date.strftime("yesterday %H:%M")
    else:
        return date.strftime("%H:%M")

class Controller(object):
    def __init__(self, master_ip, master_port, max_clients):
    
        self.authentication_model = AuthenticationModel()
        self.servers_model = ServersModel()
        self.socket_manager = SocketManager(master_ip, master_port, max_clients)
        
        #######################################
        #connect up our signals
        #######################################
        
        #SocketManager
        
        self.socket_manager.started.connect(self.on_started)
        self.socket_manager.stopped.connect(self.on_stopped)
        self.socket_manager.connect.connect(self.on_connect)
        self.socket_manager.request.connect(self.on_request)
        self.socket_manager.disconnect.connect(self.on_disconnect)
        
        #AuthenticationModel
        
        self.authentication_model.challenge.connect(self.on_auth_challenge)
        self.authentication_model.accept.connect(self.on_auth_accept)
        self.authentication_model.deny.connect(self.on_auth_deny)
        
        #######################################
        #start up the socket_manager
        #######################################
        
        self.socket_manager.run()
        
    def on_started(self, ip, port):
        print "Master server started."
        print "Listening on (%s, %s)." %(str(ip), str(port))
        print "Press Ctrl-c to exit."
        
    def on_stopped(self):
        print "\nMaster server stopped."
        
    def on_connect(self, client):
        print "client connected %s" % str(client.address)
    
    def on_request(self, client, data):
        print "client request %s:" % str(client.address), data
        
        if len(data) <= 0:
            return
        
        if data[0] == "list":
            servers_list = self.servers_model.get_server_list()
            client.send(servers_list)
        elif data[0] == "regserv":
            try:
                port = int(data[1])
                self.servers_model.register_server(client, port)
            except (IndexError, ValueError):
                return
        elif data[0] == "reqauth":
            try:
                authid = int(data[1])
                member_name = data[2]
                self.authentication_model.request_authentication(client, authid, member_name)
            except (IndexError, ValueError):
                return
        elif data[0] == "confauth":
            try:
                authid = int(data[1])
                response = data[2]
                self.authentication_model.confirm_authentication(client, authid, response)
            except (IndexError, ValueError):
                return
        elif data[0] == "names":
            try:
                reqid = int(data[1])
                ip = int(data[2])
                mask = int(data[3])
                
                result_string_parts = []
                
                results = IpName.fetch(ip, mask)
                
                for result in results:
                    result_string_parts.extend([cs_escape(result.name), format_date(result.date), result.count])
                    
                result_string_parts = map(str, result_string_parts)
                    
                result_string = '" "'.join(result_string_parts)
                    
                client.send("names {} \"{}\"\n".format(reqid, result_string))
            except (IndexError, ValueError):
                return
            
        elif data[0] == "recname":
            try:
                name = data[1]
                ip = int(data[2])
                IpName.record(name, ip)
            except (IndexError, ValueError):
                return
    
    def on_disconnect(self, client):
        self.servers_model.remove_server(client)
        print "client disconnected %s" % str(client.address)
    
    def on_auth_challenge(self, client, authid, challenge):
        message = "chalauth %s %s\n" % (authid, challenge)
        client.send(message)
    
    def on_auth_accept(self, client, authid, display_name, groups):
        def remove_spaces(string):
            return string.translate(None, ' ')
            
        display_name = remove_spaces(display_name)
        groups = map(remove_spaces, groups)
        
        message = "succauth {} {} {}\n".format(authid, display_name, ' '.join(groups))
        client.send(message)
    
    def on_auth_deny(self, client, authid):
        message = "failauth {}\n".format(authid)
        client.send(message)
        
