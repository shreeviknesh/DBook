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