class Database:
    def __init__(self, parentself):
        self.parent = parentself

        from credentials import DB_CREDENTIALS
        self.credentials = DB_CREDENTIALS