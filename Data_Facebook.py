class Facebook:
    def __init__(self, parentself):
        self.parent = parentself
        
        from credentials import FB_CREDENTIALS
        self.credentials = FB_CREDENTIALS