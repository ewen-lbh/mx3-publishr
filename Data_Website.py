class Website:
    def __init__(self, parentself):
        self.parent = parentself

        from credentials import FTP_CREDENTIALS
        self.credentials = FTP_CREDENTIALS