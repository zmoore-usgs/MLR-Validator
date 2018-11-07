import requests

class CruValidator:
    '''
    Validates the document against data from the MLR CRU service.
    '''
    MISSING_NORMALIZED_STATION_NAME = 'missing_normalized_station_name'
    DUPLICATE_NORMALIZED_STATION_NAME = 'duplicate_normalized_station_name'
    MISSING_IDENTIFYING_ATTRIBUTES = 'missing_identifying_attributes'
    _NORMALIZED_STATION_NAME_ATTRIBUTE = 'stationIx'

    def __init__(self, cru_service_url):
        """
        :param cru_service_url: a string URL describing a CRU service endpoint. No trailing slashes
        """
        self._errors = {}
        self._cru_service_url = cru_service_url

    @property
    def errors(self):
        return self._errors

    def _append_error(self, error_type, error_message):
        if error_type not in self.errors:
            self.errors[error_type] = []
        self.errors[error_type].append(error_message)

    def validate(self, document, update=False):
        """
        Validates the parameterized document and adds any errors to this instance's `errors` property
        :param document: a dict describing a monitoring location creation or update
        :param update: Boolean True if it's an update, False if it's a creation
        :return: Boolean True if valid, False if invalid
        """
        valid = self.validate_normalized_station_name(document, update)
        return valid

    def get_mls_by_normalized_station_name(self, normalized_station_name):
        """
        :param normalized_station_name: the string normalized station name
        :return: a list of dictionaries that represent monitoring locations
        """
        params = {'normalizedStationName': normalized_station_name}
        response = requests.get(self._cru_service_url + '/monitoringLocations', params=params)
        if 200 == response.status_code:
            monitoring_locations = response.json()
        else:
            monitoring_locations = []

        return monitoring_locations

    def validate_normalized_station_name(self, document, update):
        """
        Checks the CRU service to see if any existing normalized station names (aka stationIx) match the normalized
        station name in the parameterized document. Validates document differently depending on whether it is an
        "update" or a create.
        :param document: a dict describing a monitoring location creation or update
        :param update: Boolean True if `document` is an update. False if document is an add.
        :return: Boolean True if valid. False if invalid.
        """
        if update:
            valid = self._validate_normalized_station_name_update(document)
        else:
            #it's a creation!
            valid = self._validate_normalized_station_name_creation(document)
        return valid

    def _validate_normalized_station_name_update(self, document):
        """
        Checks to see if the parameterized document is a valid update. If the document specifies a normalized station
        name (aka stationIx), then it checks to see if any existing monitoring locations have the same
        normalized station name.
        :param document: a dict describing a monitoring location update
        :return: Boolean True if valid. False if invalid.
        """
        if CruValidator._NORMALIZED_STATION_NAME_ATTRIBUTE in document:
            mls = self.get_mls_by_normalized_station_name(document[CruValidator._NORMALIZED_STATION_NAME_ATTRIBUTE])
            valid = self._is_valid_normalized_station_name_update(document, mls)
            if not valid:
                msg = self._make_duplicate_normalized_station_name_error_message(document, mls)
                self._append_error(CruValidator.DUPLICATE_NORMALIZED_STATION_NAME, msg)
        else:
            valid = True

        return valid

    def _validate_normalized_station_name_creation(self, document):
        """
        Checks to see if the parameterized document is a valid addition. Checks to see if any existing station names
        (aka stationIx) match the normalized station name.
        :param document: a dict
        :return: Boolean True if valid. False if invalid.
        """
        if CruValidator._NORMALIZED_STATION_NAME_ATTRIBUTE in document:
            mls = self.get_mls_by_normalized_station_name(document[CruValidator._NORMALIZED_STATION_NAME_ATTRIBUTE])
            valid = 0 == len(mls)
            if not valid:
                msg = self._make_duplicate_normalized_station_name_error_message(document, mls)
                self._append_error(CruValidator.DUPLICATE_NORMALIZED_STATION_NAME, msg)
        else:
            valid = False
            msg = "The new monitoring location was missing the required '{}' field. {}".format(
                CruValidator._NORMALIZED_STATION_NAME_ATTRIBUTE,
                document
            )
            self._append_error(CruValidator.MISSING_NORMALIZED_STATION_NAME, msg)

        return valid

    def _is_valid_normalized_station_name_update(self, document, related_mls):
        """
        The document is considered valid iff there is a single related station with the same `siteNumber` and
        'agencyCode' values.
        :param related_mls: list of dicts describing monitoring locations with the same normalized station name
        :return: Boolean True if valid, False if invalid
        """
        valid = True
        if 1 == len(related_mls):
            # It's ok if they have the same siteNumber and agency code. It's bad if they are different
            other_ml = related_mls[0]
            valid = self._same_ml(document, other_ml)
        elif 1 < len(related_mls):
            # The update's name collides with more than one record's normalized name. This can't be valid.
            valid = False
            msg = self._make_duplicate_normalized_station_name_error_message(document, related_mls)
            self._append_error(CruValidator.DUPLICATE_NORMALIZED_STATION_NAME, msg)

        return valid

    def _same_ml(self, proposed_ml, existing_ml):
        """
        Checks whether two monitoring locations are the same by comparing their 'agencyCode' and 'siteNumber' fields.
        Side effects: modifies self.errors if the parameters are missing information or if they aren't the same
        monitoring location
        :param proposed_ml: a dict describing a monitoring location
        :param existing_ml: a dict describing a monitoring location
        :return: True if both monitoring locations are the same. False otherwise.
        """
        if not self._ml_has_identifying_attributes(proposed_ml):
            msg = self._make_missing_identifying_attributes_message(proposed_ml)
            self._append_error(CruValidator.MISSING_IDENTIFYING_ATTRIBUTES, msg)
            same = False
        elif not self._ml_has_identifying_attributes(existing_ml):
            msg = self._make_missing_identifying_attributes_message(existing_ml)
            self._append_error(CruValidator.MISSING_IDENTIFYING_ATTRIBUTES, msg)
            same = False
        else:
            same = proposed_ml['siteNumber'] == existing_ml['siteNumber'] and \
                   proposed_ml['agencyCode'] == existing_ml['agencyCode']
            if not same:
                msg = self._make_duplicate_normalized_station_name_error_message(proposed_ml, [existing_ml])
                self._append_error(CruValidator.DUPLICATE_NORMALIZED_STATION_NAME, msg)

        return same

    def _ml_has_identifying_attributes(self, ml):
        """
        :param ml: a dict describing a monitoring location
        :return: Boolean True if the monitoring location has identifying attributes, False otherwise.
        """
        has_identifying_attributes = 'siteNumber' in ml and 'agencyCode' in ml
        return has_identifying_attributes

    def _make_missing_identifying_attributes_message(self, ml):
        """
        :param ml: a dict representing a monitoring location
        :return: str error message
        """
        return "The following monitoring location lacks the identifying 'siteNumber' and 'agencyCode' attributes, {}".format(ml)

    def _make_duplicate_normalized_station_name_error_message(self, document, duplicates):
        """
        :param document: the document being validated
        :param duplicates: the duplicates found
        :return:
        """
        normalized_station_name = document[CruValidator._NORMALIZED_STATION_NAME_ATTRIBUTE]

        msg = "The submitted normalized station name ({}) field ({})"
        msg += " matches that of the following existing {} record(s):\n"
        msg = msg.format(
            CruValidator._NORMALIZED_STATION_NAME_ATTRIBUTE,
            normalized_station_name,
            len(duplicates)
        )
        duplicates_as_str = [str(duplicate) for duplicate in duplicates]
        msg += "\n".join(duplicates_as_str)
        return msg
