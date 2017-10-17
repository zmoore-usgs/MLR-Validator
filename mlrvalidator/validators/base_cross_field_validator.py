
from cerberus import Validator

class BaseCrossFieldValidator(Validator):
    '''
    Extends validate to add an argument for the existing_document. Typically for an add this will be empty.
    '''

    def validate(self, document, existing_document, schema=None, update=False, normalize=True):
        self.merged_document = existing_document.copy()
        self.merged_document.update(document)

        return Validator.validate(self, document, schema=schema, update=update, normalize=normalize)
