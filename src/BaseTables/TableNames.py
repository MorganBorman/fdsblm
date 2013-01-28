prefix = "smf_"

table_names = {}

table_names['Member']               = 'members'
table_names['MemberGroup']          = 'membergroups'
table_names['Theme']                = 'themes'
table_names['IpName']               = 'sb_srv_ipnames'
table_names['PunitiveEffect']       = 'sb_srv_punitive_effects'

for key in table_names.keys():
    table_names[key] = prefix + table_names[key]

