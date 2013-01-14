#!/usr/bin/python

import sys

id_member = int(sys.argv[1])

if id_member < 0:
    print "Member ids must be positive."
    sys.exit(-1)

import random
import cube2crypto

from BaseTables import Member, MemberGroup

member = Member.by_member_id(id_member)

if member is None:
    print "Could not retrieve member."
    sys.exit(-1)

member.private_auth_key, member.public_auth_key = cube2crypto.genkeypair(format(random.getrandbits(128), 'X'))

print "Successfully updated auth keys."

sys.exit(0)
