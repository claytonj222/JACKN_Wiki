def findActiveUsers(users):
    names = users.keys()
    listofusers = []
    for name in names:
        if users[name]['active']:
            listofusers.append(name)
    return listofusers
