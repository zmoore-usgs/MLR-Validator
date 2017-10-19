
class LegacyObjectValidator:

    def __init__(self):
        self.errors = ''

    def validate(self, ddot_location, existing_location):
        self.errors = ''
        return True

    def get_errors(self):
        return self.errors