"""Represents the body of the server list data."""

import time

class ServersModel(object):
    def __init__(self):
        self.server_list = ""
        self.server_list_dirty = True
        
        #key = client
        #value = (port, time, server_domain)
        self.servers = {}
        
    def register_server(self, client, port):
        "Attempt to register a newly connected server_domain."
        
        if client in self.servers.keys():
            self.servers[client]['time'] = time.time()
            return
        
        self.servers[client] = {'port': port, 'time': time.time()}
        self.server_list_dirty = True
        
    def is_server_confirmed(self, client):
        "Check whether the specified server has been confirmed."
        return client in self.servers.keys()
        
    def remove_server(self, client):
        "Removed the specified server from the list."
        if client in self.servers.keys():
            del self.servers[client]
            self.server_list_dirty = True
        
    def refresh(self):
        "Look for servers which have timed out."
        pass
        
    def get_server_list(self):
        "Get the current list of servers."
        if self.server_list_dirty:
            server_list_list = []
            for client, data in self.servers.items():
                server_ip = client.address[0]
                server_port = data['port']
                server_list_list.append("addserver %s %s\n" %(server_ip, server_port))
            self.server_list = "".join(server_list_list)
            self.server_list_dirty = False
            
        return self.server_list
        
    def broadcast(self, data):
        "Send a message to all servers."
        for client in self.servers.keys():
            client.send(data)

