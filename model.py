class User:
    def __init__(self, username, password, unique):
        self.username = username
        self.password = password
        self.unique = unique

    def add_to_db(self):
        global users
        users.insert({
            'username': self.username,
            'password': self.password,
            'unique': self.unique
        })
    
    def add_item(self, dictionary, key, value):
        dictionary.update({
            key:{
                'artist':value['artist'],
                'album':value['album'],
                'giving':value['giving'],
                'getting':value['getting'],
                'account':value['account'],
                'platform':value['platform'],
                'date':value['date']
            }
        })