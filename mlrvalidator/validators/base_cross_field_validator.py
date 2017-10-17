
from cerberus import Validator

class BaseCrossFieldValidator(Validator):
    '''
    Extends validate to add an argument for the existing_document. Typically for an add this will be empty.
    '''

    def validate(self, document, existing_document, schema=None, update=False, normalize=True):
        self.existing_document = existing_document
        self.merged_document = existing_document.copy()
        self.merged_document.update(document)

        return super().validate(document, schema=schema, update=update, normalize=normalize)
