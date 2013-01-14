from Signals import SignalObject, Signal

import random
import cube2crypto

from BaseTables import Member, MemberGroup

class AuthenticationModel(SignalObject):

    challenge = Signal
    accept = Signal
    deny = Signal

    def __init__(self):
        SignalObject.__init__(self)
        
        #key = (client, authid)
        #value = {'member': Member, 'answer': answer}
        self.pending_auths = {}
        
    def request_authentication(self, client, authid, member_name):
        
        if "@" in member_name:
            member = Member.by_member_email(member_name)
        else:
            member = Member.by_member_name(member_name)
        
        if member is None:
            print "Could not fetch member. Failing authentication."
            self.deny.emit(client, authid)
            return
        
        pubkey = member.public_auth_key
        
        if pubkey is None:
            print "Could not fetch pubkey. Failing authentication."
            self.deny.emit(client, authid)
            return
        
        challenge, answer = cube2crypto.genchallenge(pubkey, format(random.getrandbits(128), 'X'))
        
        self.pending_auths[(client, authid)] = {'member': member, 'answer': answer}
        
        self.challenge.emit(client, authid, challenge)
        
    def confirm_authentication(self, client, authid, answer):
        
        if not (client, authid) in self.pending_auths.keys():
            self.deny.emit(client, authid)
            return
        
        pending_auth = self.pending_auths[(client, authid)]
        member = pending_auth['member']
        
        if answer != pending_auth['answer']:
            self.deny.emit(client, authid)
        else:
            self.accept.emit(client, 
                             authid, 
                             member.real_name,
                             member.group_list)

