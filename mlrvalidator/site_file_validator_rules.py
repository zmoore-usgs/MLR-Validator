
import datetime
import re

from cerberus import Validator

from .land_net_templates import land_net_ref


class SitefileValidator(Validator):
    def _validate_type_numeric(self, value):
        # check for numeric value
        try:
            float(value)
        except ValueError:
            return False

        return True

    def _validate_type_positive_numeric(self, value):
        # check for positive numeric value
        try:
            test_num = float(value)
        except ValueError:
            return False

        if test_num < 0:
            return False
        else:
            return True

    def _validate_valid_precision(self, valid_precision, field, value):
        """
        # Check that precision is no more than 2 decimal places

        The rule's arguments are validated against this schema:
        {'valid_valid_precision': False}
        """
        error_message = "Invalid Value, decimal precision error"

        stripped_value = value.strip()
        test_split = stripped_value.split(".")
        # there is a decimal, so need to check what's after it
        if len(test_split) > 1:
            if test_split[1] == "":
                self._error(field, error_message)
            else:
                # Check that only digits 0-9 exist after the decimal
                test_field = re.search('[^0-9]+', test_split[1])
                if test_field is not None:
                    # There is something besides digits 0-9 after the decimal
                    self._error(field, error_message)
                if len(test_split[1]) > 2:
                    self._error(field, error_message)

    def _validate_is_empty(self, is_empty, field, value):
        """
        # Since the value coming in could consist of spaces, check that a value of only spaces is considered null

        The rule's arguments are validated against this schema:
        {'valid_is_empty': False}
        """
        stripped_value = value.strip()
        if not is_empty:
            if not stripped_value:
                self._error(field, "Mandatory Field Missing")

    def _validate_valid_special_chars(self, valid_special_chars, field, value):
        """
        # Check that tab, #, *, \, ", ^, _, and $ do not exist in field

        The rule's arguments are validated against this schema:
        {'valid_special_chars': True}
        """
        if valid_special_chars:
            test_field = re.search(r'[\t#*\\\"^_$]+', value)
            if test_field is not None:
                self._error(field, "Invalid Character: contains tab, #, *, \, "", ^, _, or $")

    def _validate_valid_map_scale_chars(self, valid_map_scale_chars, field, value):
        """
        # Check that characters other than 0-9 or a blank space do not exist in field

        The rule's arguments are validated against this schema:
        {'valid_map_scale_chars': True}
        """
        if valid_map_scale_chars:
            test_field = re.search('[^0-9 ]+', value)
            if test_field is not None:
                # There is something besides digits 0-9 or space
                self._error(field, "Invalid Character: contains a character other than 0-9")

    def _validate_valid_instruments_chars(self, valid_instruments_chars, field, value):
        """
        # Check that characters other than Y, N, or a blank space do not exist in field

        The rule's arguments are validated against this schema:
        {'valid_instruments_chars': True}
        """
        if valid_instruments_chars:
            if not all(c.upper() in "YN " for c in value):
                self._error(field, "Invalid Character: contains a character other than Y, N, or a blank space")

    def _validate_valid_data_types_chars(self, valid_data_types_chars, field, value):
        """
        # Check that character other than A, I, O, N, or a blank space do not exist in field

        The rule's arguments are validated against this schema:
        {'valid_data_types_chars': True}
        """
        if valid_data_types_chars:
            if not all(c.upper() in "AION " for c in value):
                self._error(field, "Invalid Character: contains a character other than A, I, O, N, or a blank space")

    def _validate_valid_latitude_dms(self, valid_latitude_dms, field, value):
        # Check that field consists of valid degrees, minutes and second values

        """
        The rule's arguments are validated against this schema:
        {'valid_latitude_dms': True}
        """
        error_message = "Invalid Degree/Minute/Second Value"
        rstripped_value = value.rstrip()

        def check_100th_seconds(val):
            try:
                val[7] in ["."]
                test_split = val.split(".")
                # There is a decimal, but have to check if anything was split from it
                if test_split[1] == "":
                    return False
                else:
                    # Check that only digits 0-9 exist after the decimal
                    test_field = re.search('[^0-9]+', test_split[1])
                    if test_field is None:
                        # There are only digits 0-9 after the decimal
                        return True
                    else:
                        # There is something besides digits 0-9 after the decimal
                        return False
            except IndexError:
                return True

        if valid_latitude_dms:
            try:
                first_val = rstripped_value[0]
                check_degrees = rstripped_value[1:3]
                check_minutes = rstripped_value[3:5]
                check_seconds = rstripped_value[5:7]
            except IndexError:
                return self._error(field, error_message)

            try:
                if not ((first_val in "- ") and (0 <= int(check_degrees) <= 90) and (
                        0 <= int(check_minutes) < 60) and (0 <= int(check_seconds) < 60)
                        and check_100th_seconds(rstripped_value)):
                    self._error(field, error_message)
            except ValueError:
                return self._error(field, error_message)

    def _validate_valid_longitude_dms(self, valid_longitude_dms, field, value):
        # Check that field consists of valid degrees, minutes and second values

        """
        The rule's arguments are validated against this schema:
        {'valid_longitude_dms': True}
        """
        error_message = "Invalid Degree/Minute/Second Value"
        rstripped_value = value.rstrip()

        def check_100th_seconds(val):
            try:
                val[8] in ["."]
                test_split = val.split(".")
                # There is a decimal, but have to check if anything was split from it
                if test_split[1] == "":
                    return False
                else:
                    # Check that only digits 0-9 exist after the decimal
                    test_field = re.search('[^0-9]+', test_split[1])
                    if test_field is None:
                        # There are only digits 0-9 after the decimal
                        return True
                    else:
                        # There is something besides digits 0-9 after the decimal
                        return False
            except IndexError:
                return True

        if valid_longitude_dms:
            try:
                first_val = rstripped_value[0]
                check_degrees = rstripped_value[1:4]
                check_minutes = rstripped_value[4:6]
                check_seconds = rstripped_value[6:8]
            except IndexError:
                return self._error(field, error_message)
            try:
                if not ((first_val in "- ") and (0 <= int(check_degrees) <= 180) and (
                        0 <= int(check_minutes) < 60) and (0 <= int(check_seconds) < 60)
                        and check_100th_seconds(rstripped_value)):
                    self._error(field, error_message)
            except ValueError:
                return self._error(field, error_message)

    def _validate_valid_date(self, valid_date, field, value):
        # Check that field is a formatted date of YYYY, YYYYMM or YYYYMMDD

        """
        The rule's arguments are validated against this schema:
        {'valid_date': True}
        """
        error_message = "Invalid Date, should be YYYY, YYYYMM or YYYYMMDD"
        stripped_value = value.strip()
        if valid_date:
        # Check for valid full or partial date lengths
            if len(stripped_value) in [8, 6, 4]:
                # Check that only digits 0-9 exist in the string
                test_field = re.search('[^0-9]+', stripped_value)
                if test_field is None:
                    # There are only digits 0-9 in the string
                    check_year = stripped_value[0:4]
                    check_month = stripped_value[4:6]
                    if not 1582 <= int(check_year) <= int(datetime.date.today().year):
                        self._error(field, error_message)
                    if len(stripped_value) == 8:
                        try:
                            valid_date = datetime.datetime.strptime(stripped_value, '%Y%m%d')
                        except ValueError:
                            return self._error(field, error_message)
                    if check_month:
                        if not 1 <= int(check_month) <= 12:
                            self._error(field, error_message)

                else:
                    self._error(field, error_message)
            else:
                self._error(field, error_message)

    def _validate_valid_land_net(self, valid_land_net, field, value):
        # Check that the land net description field follows the correct template

        """
        The rule's arguments are validated against this schema:
        {'valid_land_net': True}
        """
        error_message = "Invalid format - Land Net does not fit template"

        if valid_land_net:
            land_net_template = land_net_ref["55"]
            value_end = len(value) - 1
            section = land_net_template.index("S")
            township = land_net_template.index("T")
            range = land_net_template.index("R")
            try:
                if not (value[section] == "S" and value[township] == "T" and value[range] == "R"):
                    return self._error(field, error_message)
                test_match = re.search('[^a-zA-Z0-9 ]', value[section:value_end])
                if test_match is not None:
                    return self._error(field, error_message)
            except IndexError:
                return self._error(field, error_message)

    def _validate_lat_long(self, lat_long, field, value):
        # Check that if latitude was entered, so was longitude, and vice versa

        """
        The rule's arguments are validated against this schema:
        {'lat_long': True}
        """
        if lat_long:
            try:
                if self.document['latitude']:
                    if not self.document['longitude']:
                        return self._error(field, "Latitude entered without longitude")
                if self.document['longitude']:
                    if not self.document['latitude']:
                        return self._error(field, "Longitude entered without latitude")
            except KeyError:
                return self._error(field, "Key not found in dictionary")

    def _validate_allowed_coord_acy_cd(self, allowed_coord_acy_cd, field, value):
        # Check if coord_acy_cd was entered, so were latitude and longitude

        """
        The rule's arguments are validated against this schema:
        {'allowed_coord_acy_cd': True}
        """
        if allowed_coord_acy_cd:
            if self.document['latitude'] and self.document['longitude']:
                if not self.document['coordinateAccuracyCode']:
                    return self._error(field, "Coordinate accuracy code required if latitude and longitude are entered")

    def _validate_allowed_coord_datum_cd(self, allowed_coord_datum_cd, field, value):
        # Check if coord_datum_cd was entered, so were latitude and longitude

        """
        The rule's arguments are validated against this schema:
        {'allowed_coord_datum_cd': True}
        """
        if allowed_coord_datum_cd:
            if self.document['latitude'] and self.document['longitude']:
                if not self.document['coordinateDatumCode']:
                    return self._error(field, "Coordinate datum code required if latitude and longitude are entered")

    def _validate_allowed_coord_meth_cd(self, allowed_coord_meth_cd, field, value):
        # Check if coord_meth_cd was entered, so were latitude and longitude

        """
        The rule's arguments are validated against this schema:
        {'allowed_coord_meth_cd': True}
        """
        if allowed_coord_meth_cd:
            if self.document['latitude'] and self.document['longitude']:
                if not self.document['coordinateMethodCode']:
                    return self._error(field, "Coordinate method code required if latitude and longitude are entered")

    def _validate_valid_alt_datum_cd(self, valid_alt_datum_cd, field, value):
        # Check if altitude was entered, so was altitude datum code

        """
        The rule's arguments are validated against this schema:
        {'valid_alt_datum_cd': True}
        """
        if valid_alt_datum_cd:
            if self.document['altitude']:
                if not self.document['altitudeDatumCode']:
                    return self._error(field, "Altitude entered without altitude datum code")

    def _validate_valid_alt_meth_cd(self, valid_alt_meth_cd, field, value):
        # Check if altitude was entered, so was altitude method code

        """
        The rule's arguments are validated against this schema:
        {'valid_alt_meth_cd': True}
        """
        if valid_alt_meth_cd:
            if self.document['altitude']:
                if not self.document['altitudeMethodCode']:
                    return self._error(field, "Altitude entered without altitude method code")

    def _validate_valid_alt_acy_va(self, valid_alt_acy_va, field, value):
        # Check if altitude was entered, so was altitude accuracy value

        """
        The rule's arguments are validated against this schema:
        {'valid_alt_acy_va': True}
        """
        if valid_alt_acy_va:
            if self.document['altitude']:
                if not self.document['altitudeAccuracyValue']:
                    return self._error(field, "Altitude entered without altitude accuracy value")

    def _validate_valid_site_use_cd(self, valid_site_use_cd, field, value):
        # Check that site use codes 1, 2, and 3 have different values if more than one is entered
        # Check that site use code 2 is null if code 1 is null
        # Check that site use code 3 is null if code 2 is null
        """
        The rule's arguments are validated against this schema:
        {'valid_site_use_cd': True}
        """
        if valid_site_use_cd:
            if self.document['primaryUseOfSite'] and self.document['secondaryUseOfSite']:
                if self.document['primaryUseOfSite'] == self.document['secondaryUseOfSite']:
                    return self._error(field, "Site use codes 1, 2, and 3 must have different values if more than one is entered")
                if self.document['tertiaryUseOfSiteCode']:
                    if self.document['primaryUseOfSite'] == self.document['tertiaryUseOfSiteCode'] or self.document['secondaryUseOfSite'] == self.document['tertiaryUseOfSiteCode']:
                        return self._error(field, "Site use codes 1, 2, and 3 must have different values if more than one is entered")
            if not self.document['primaryUseOfSite']:
                if self.document['secondaryUseOfSite']:
                    return self._error(field, "Site use code 2 must be null if site use code 1 is null")
            if not self.document['secondaryUseOfSite']:
                if self.document['tertiaryUseOfSiteCode']:
                    return self._error(field, "Site use code 3 must be null if site use code 2 is null")

    def _validate_valid_water_use_cd(self, valid_water_use_cd, field, value):
        # Check that water use codes 1, 2, and 3 have different values if more than one is entered
        # Check that water use code 2 is null if code 1 is null
        # Check that water use code 3 is null if code 2 is null
        """
        The rule's arguments are validated against this schema:
        {'valid_water_use_cd': True}
        """
        if valid_water_use_cd:
            if self.document['primaryUseOfWaterCode'] and self.document['secondaryUseOfWaterCode']:
                if self.document['primaryUseOfWaterCode'] == self.document['secondaryUseOfWaterCode']:
                    return self._error(field, "Water use codes 1, 2, and 3 must have different values if more than one is entered")
                if self.document['tertiaryUseOfWaterCode']:
                    if self.document['primaryUseOfWaterCode'] == self.document['tertiaryUseOfWaterCode'] or self.document['secondaryUseOfWaterCode'] == self.document['tertiaryUseOfWaterCode']:
                        return self._error(field, "Water use codes 1, 2, and 3 must have different values if more than one is entered")
            if not self.document['primaryUseOfWaterCode']:
                if self.document['secondaryUseOfWaterCode']:
                    return self._error(field, "Water use code 2 must be null if site use code 1 is null")
            if not self.document['secondaryUseOfWaterCode']:
                if self.document['tertiaryUseOfWaterCode']:
                    return self._error(field, "Water use code 3 must be null if site use code 2 is null")

    def _validate_const_inv_dts(self, const_inv_dts, field, value):
        # Check that construction_dt is not > inventory_dt
        """
        The rule's arguments are validated against this schema:
        {'const_inv_dts': True}
         """
        if const_inv_dts:
            try:
                if self.document['firstConstructionDate'] and self.document['siteEstablishmentDate']:
                    if self.document['firstConstructionDate'] > self.document['siteEstablishmentDate']:
                        return self._error(field, "Construction date cannot be more recent than inventory date")
            except KeyError:
                return self._error(field, "Key not found in dictionary")


    def _validate_well_hole_depths(self, well_hole_depths, field, value):
        # Check that well depth is not > hole depth
        """
        The rule's arguments are validated against this schema:
        {'well_hole_depths': True}
         """
        if well_hole_depths:
            if self.document['wellDepth'] and self.document['holeDepth']:
                if self.document['wellDepth'] > self.document['holeDepth']:
                    return self._error(field, "Well depth cannot be greater than hole depth")





