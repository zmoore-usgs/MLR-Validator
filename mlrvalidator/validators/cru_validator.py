import requests


class CruValidator:
    '''
    Validates the document against data from the MLR CRU service.
    '''
    DUPLICATE_NORMALIZED_STATION_NAME = 'duplicate_normalized_station_name'

    def __init__(self, cru_service_url):
        """
        :param cru_service_url: a string URL describing a CRU service endpoint. No trailing slashes
        """
        self._errors = {}
        self._cru_service_url = cru_service_url

    @property
    def errors(self):
        return self._errors

    def _make_duplicate_normalized_station_error_message(self, document, duplicates):
        """
        :param document: the document being validated
        :param duplicates: the duplicates found
        :return:
        """
        normalized_station_name = document['stationIx']

        msg = "The submitted normalized station name (stationIx) field ({})"
        msg += " matches that of the following existing {} record(s):\n"
        msg = msg.format(
            normalized_station_name,
            len(duplicates)
        )
        duplicates_as_str = [str(duplicate) for duplicate in duplicates]
        msg += "\n".join(duplicates_as_str)
        return msg

    def _is_update(self, document):
        """
        :param document: a dict describing a monitoring location creation or update
        :return: Boolean true if the document is an update, false otherwise
        """
        #is_update = 'id' in document and None != document['id']
        is_update = 'M' == document['transactionType']
        return is_update

    def validate(self, document):
        """
        Validates the parameterized document and adds any errors to this instance's `errors` property
        :param document: a dict describing a monitoring location creation or update
        :return: Boolean True if valid, False if invalid
        """
        valid = self.validate_normalized_station_name(document)
        return valid

    def get_stations_by_normalized_name(self, normalized_name):
        """
        :param normalized_name: the string normalized station name
        :return: a list of dictionaries that represent monitoring locations
        """
        params = {'normalizedStationName': normalized_name}
        response = requests.get(self._cru_service_url + '/monitoringLocations', params=params)
        if 200 == response.status_code:
            stations = response.json()
        else:
            stations = []

        return stations

    def validate_normalized_station_name(self, document):
        """
        Checks the CRU service to see if any existing normalized station names (aka stationIx) match the normalized
        station name in the parameterized document. Validates document differently depending on whether it is an
        "update" or a create.
        :param document: a dict describing a monitoring location creation or update
        :return: Boolean True if valid. False if invalid.
        """
        normalized_station_name = document['stationIx']
        stations = self.get_stations_by_normalized_name(normalized_station_name)
        valid = self._validate_normalized_station_name(document, stations)
        return valid


    def _validate_normalized_station_name(self, document, stations):
        """
        Checks to see if any existing station names (aka stationIx) match the normalized
        station name in the parameterized document. Validates document differently depending on whether it is an
        "update" or a create.
        :param document: a dict describing a monitoring location creation or update
        :param stations: list of dicts describing monitoring locations with the same normalized station name
        :return:
        """
        is_update = self._is_update(document)

        if is_update:
            valid = self._is_valid_normalized_station_name_update(document, stations)
        else:
            # it's a create!
            valid = 0 == len(stations)

        if not valid:
            msg = self._make_duplicate_normalized_station_error_message(document, stations)
            self._errors[CruValidator.DUPLICATE_NORMALIZED_STATION_NAME] = msg

        return valid

    def _is_valid_normalized_station_name_update(self, document, related_stations):
        """
        The document is considered valid iff the CRU service returns
        a single matching record with the same `id` property.
        :param related_stations: list of dicts describing monitoring locations with the same normalized station name
        :return: Boolean True if valid, False if invalid
        """
        valid = True
        if 1 == len(related_stations):
            # It's ok if they have the same siteNumber and agency code. It's bad if they are different
            other_station = related_stations[0]
            if document['siteNumber'] != other_station['siteNumber'] or \
               document['agencyCode'] != other_station['agencyCode']:
                valid = False
        elif 1 < len(related_stations):
            # The update's name collides with more than one record's normalized name. This can't be valid.
            valid = False
        return valid


