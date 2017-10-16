from cerberus import Validator


class CrossFieldValidator(Validator):

    def validate(self, document, existing_document, schema=None, update=False, normalize=True):
        self.merged_document = existing_document.copy()
        self.merged_document.update(document)

        return Validator.validate(self, document, schema=schema, update=update, normalize=normalize)


    def _validate_reciprocal_dependency(self, dependent_list, field, value):

        """
        Validates if value exists and all values for fields in dependent_list exist or if value is empty and
        all values for fields in dependent_list are empty

        The rule's arguments are validated against this schema:
        {'type': 'list', schema: {'type': 'string'}
        """
        for dependent_field in dependent_list:
            dependent_value = self.merged_document.get(dependent_field, '')
            value_is_empty = not value.strip()
            dependent_value_is_empty = not dependent_value.strip()
            if value_is_empty and not dependent_value_is_empty:
                self._error(field, '{0} can not be null when {1} is not null'.format(field, dependent_field))
            elif not value_is_empty and dependent_value_is_empty:
                self._error(field, '{0} can not have a value when {1} is null'.format(field, dependent_field))


    def _validate_unique_use_value(self, field_to_check, field, value):
        """
        Validates if value is empty or if not empty is different from field_to_check's value

        The rule's arguments are validated against this schema:
        {'type': 'string'}
        """
        field_value = value.strip()
        field_to_check_value = self.merged_document.get(field_to_check, '').strip()
        if field_value and (field_value == field_to_check_value):
            self._error(field, '{0} must not have the same value as {1}'.format(field, field_to_check))


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