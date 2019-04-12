def findUserByName(mongo, username):
    query = {"username": username}
    return mongo.db.users.find_one(query)


def insertUser(mongo, form):
    user = {
        "username": form['username'], 
        "password": form['password'],
        "email": form['email'],
        "phone": form['phone'],
        "friends": [],
        "numFriends": 0
    }
    return mongo.db.users.insert_one(user)

def findAllUsers(mongo):
    allUsers = mongo.db.users.find({})
    return list(allUsers)

def addFriendToUser(mongo, user, friend):
    findQuery = {"username": user}
    user_document = mongo.db.users.find_one(findQuery)
    friends = user_document['friends']

    friends.append(friend)
    numFriends = len(friends)

    updateQuery = {
        "$set": {
            "friends": friends,
            "numFriends": numFriends
        }
    }

    mongo.db.users.update_one(findQuery, updateQuery)

def findUserStartsWith(mongo, startName):
    users = findAllUsers(mongo)
    users = list(filter(lambda x: x['username'].startswith(startName), users))

    return users

def deleteUser(mongo, username):
    mongo.db.users.delete_one({'username': username})

    users = findAllUsers(mongo)

    for user in users:
        if username in user['friends']:
            friends = user['friends']
            friends.remove(username)
            numFriends = user['numFriends'] - 1

            selectQuery = {'username': user['username']}
            updateQuery = {
                '$set': {
                    'friends': friends,
                    'numFriends': numFriends
                }
            }
            mongo.db.users.update_one(selectQuery, updateQuery)
    