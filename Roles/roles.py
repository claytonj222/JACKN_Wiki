def getuserroles(users):
    names = users.keys()
    roles = []
    for name in names:
        roles.append(users[name]['roles'])
    return roles
