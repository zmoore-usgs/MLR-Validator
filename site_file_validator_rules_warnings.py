
from cerberus import Validator
import re
import datetime
from land_net_templates import land_net_ref


class SitefileWarningValidator(Validator):
    def _validate_valid_quotes(self, valid_quotes, field, value):
        """
        # Check for a single quote at the beginning at end of the incoming string

        The rule's arguments are validated against this schema:
        {'valid_quotes': True}
        """
        if valid_quotes:
            if ((value.startswith("'") and not value.endswith("'")) or
                    (not value.startswith("'") and value.endswith("'"))):
                # There is something besides digits 0-9 or space
                self._error(field, "Missing Quote -- Station Name may be missing a quote at beginning or ending of the name")
