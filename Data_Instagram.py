class Instagram:
    def __init__(self, parentself):
        self.parent = parentself

        from credentials import IG_CREDENTIALS
        self.credentials = IG_CREDENTIALS