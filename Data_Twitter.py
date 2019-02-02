class Twitter:
    def __init__(self, parentself):
        self.parent = parentself
        
        from credentials import TW_CREDENTIALS
        self.credentials = TW_CREDENTIALS