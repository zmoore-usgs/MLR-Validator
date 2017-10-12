from cerberus import Validator


class CrossFieldValidator(Validator):

    def _validate_valid_lat_long(self, valid_lat_long, field, value):
        # Check that if latitude was entered, so was longitude, and vice versa

        """
        The rule's arguments are validated against this schema:
        {'lat_long': True}
        """
        if valid_lat_long:
            if self.document['latitude']:
                if not self.document['longitude']:
                    return self._error(field, "Latitude entered without longitude")
            if self.document['longitude']:
                if not self.document['latitude']:
                    return self._error(field, "Longitude entered without latitude")

    def _validate_valid_coord_acy_cd(self, valid_coord_acy_cd, field, value):
        # Check if coord_acy_cd was entered, so were latitude and longitude

        """
        The rule's arguments are validated against this schema:
        {'allowed_coord_acy_cd': True}
        """
        if valid_coord_acy_cd:
            if self.document['latitude'] and self.document['longitude']:
                if not self.document['coordinateAccuracyCode']:
                    return self._error(field, "Coordinate accuracy code required if latitude and longitude are entered")
            if self.document['coordinateAccuracyCode']:
                if not self.document['latitude'] or not self.document['longitude']:
                    return self._error(field, "Coordinate accuracy code entered without latitude and longitude")

    def _validate_valid_coord_datum_cd(self, valid_coord_datum_cd, field, value):
        # Check if coord_datum_cd was entered, so were latitude and longitude

        """
        The rule's arguments are validated against this schema:
        {'allowed_coord_datum_cd': True}
        """
        if valid_coord_datum_cd:
            if self.document['latitude'] and self.document['longitude']:
                if not self.document['coordinateDatumCode']:
                    return self._error(field, "Coordinate datum code required if latitude and longitude are entered")
            if self.document['coordinateDatumCode']:
                if not self.document['latitude'] or not self.document['longitude']:
                    return self._error(field, "Coordinate datum code entered without latitude and longitude")

    def _validate_valid_coord_meth_cd(self, valid_coord_meth_cd, field, value):
        # Check if coord_meth_cd was entered, so were latitude and longitude

        """
        The rule's arguments are validated against this schema:
        {'allowed_coord_meth_cd': True}
        """
        if valid_coord_meth_cd:
            if self.document['latitude'] and self.document['longitude']:
                if not self.document['coordinateMethodCode']:
                    return self._error(field, "Coordinate method code required if latitude and longitude are entered")
            if self.document['coordinateMethodCode']:
                if not self.document['latitude'] or not self.document['longitude']:
                    return self._error(field, "Coordinate method code entered without latitude and longitude")

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
            if self.document['altitudeDatumCode']:
                if not self.document['altitude']:
                    return self._error(field, "Altitude datum code entered without altitude")

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
            if self.document['altitudeMethodCode']:
                if not self.document['altitude']:
                    return self._error(field, "Altitude method code entered without altitude")

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
            if self.document['altitudeAccuracyValue']:
                if not self.document['altitude']:
                    return self._error(field, "Altitude accuracy value entered without altitude")

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
                    return self._error(field,
                                       "Site use codes 1, 2, and 3 must have different values if more than one is entered")
                if self.document['tertiaryUseOfSiteCode']:
                    if (self.document['primaryUseOfSite'] == self.document['tertiaryUseOfSiteCode']
                        or self.document['secondaryUseOfSite'] == self.document['tertiaryUseOfSiteCode']
                        ):
                        return self._error(field,
                                           "Site use codes 1, 2, and 3 must have different values if more than one is entered")
            if not self.document['primaryUseOfSite']:
                if self.document['secondaryUseOfSite']:
                    return self._error(field, "Site use code 2 must be null if site use code 1 is null")
                if self.document['tertiaryUseOfSiteCode']:
                    return self._error(field, "Site use code 3 must be null if site use code 1 is null")
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
                    return self._error(field,
                                       "Water use codes 1, 2, and 3 must have different values if more than one is entered")
                if self.document['tertiaryUseOfWaterCode']:
                    if (self.document['primaryUseOfWaterCode'] == self.document['tertiaryUseOfWaterCode']
                        or self.document['secondaryUseOfWaterCode'] == self.document['tertiaryUseOfWaterCode']
                        ):
                        return self._error(field,
                                           "Water use codes 1, 2, and 3 must have different values if more than one is entered")
            if not self.document['primaryUseOfWaterCode']:
                if self.document['secondaryUseOfWaterCode']:
                    return self._error(field, "Water use code 2 must be null if water use code 1 is null")
                if self.document['tertiaryUseOfWaterCode']:
                    return self._error(field, "Water use code 3 must be null if water use code 1 is null")
            if not self.document['secondaryUseOfWaterCode']:
                if self.document['tertiaryUseOfWaterCode']:
                    return self._error(field, "Water use code 3 must be null if water use code 2 is null")

    def _validate_valid_const_inv_dts(self, valid_const_inv_dts, field, value):
        # Check that construction_dt is not > inventory_dt
        """
        The rule's arguments are validated against this schema:
        {'const_inv_dts': True}
         """
        if valid_const_inv_dts:
            if self.document['firstConstructionDate'] and self.document['siteEstablishmentDate']:
                if self.document['firstConstructionDate'] > self.document['siteEstablishmentDate']:
                    return self._error(field, "Construction date cannot be more recent than inventory date")

    def _validate_valid_well_hole_depths(self, valid_well_hole_depths, field, value):
        # Check that well depth is not > hole depth
        """
        The rule's arguments are validated against this schema:
        {'well_hole_depths': True}
         """
        if valid_well_hole_depths:
            if self.document['wellDepth'] and self.document['holeDepth']:
                if self.document['wellDepth'] > self.document['holeDepth']:
                    return self._error(field, "Well depth cannot be greater than hole depth")