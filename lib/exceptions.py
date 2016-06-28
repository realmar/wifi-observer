class InvalidConfig(Exception):
    def __init__(self, value='undefined'):
        self.value = value

    def __str__(self):
        return 'Invalid Configuration: ' + self.value
