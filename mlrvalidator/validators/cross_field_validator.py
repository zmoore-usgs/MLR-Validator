
from .base_cross_field_validator import BaseCrossFieldValidator
from . import site_type_transition_reference

class CrossFieldValidator(BaseCrossFieldValidator):

    def _validate_reciprocal_dependency(self, dependent_list, field, value):

        """
        Validates if value exists and all values for fields in dependent_list exist or if value is empty and
        all values for fields in dependent_list are empty

        The rule's arguments are validated against this schema:
        {'type': 'list'}
        """
        for dependent_field in dependent_list:
            dependent_value = self.merged_document.get(dependent_field, '')
            value_is_empty = not value.strip()
            dependent_value_is_empty = not dependent_value.strip()
            if value_is_empty and not dependent_value_is_empty:
                self._error(field, '{0} can not be null when {1} is not null'.format(field, dependent_field))
            elif not value_is_empty and dependent_value_is_empty:
                self._error(field, '{0} can not have a value when {1} is null'.format(field, dependent_field))


    def _validate_unique_use_value(self, dependent_list, field, value):
        """
        Validates if value is empty or if not empty is different from field_to_check's value

        The rule's arguments are validated against this schema:
        {'type': 'list'}
        """
        field_value = value.strip()
        for dependent_field in dependent_list:
            field_to_check_value = self.merged_document.get(dependent_field, '').strip()
            if field_value and (field_value == field_to_check_value):
                self._error(field, '{0} must not have the same value as {1}'.format(field, dependent_field))

    def _validate_not_empty_dependency(self, dependent_list, field, value):
        """
        Validates if value is empty or if value is not empty then validates if field values for fields in
        dependent_list are not empty.

        The rule's arguments are validated against this schema:
        {'type': 'list'}
        """
        field_value = value.strip()
        if field_value:
            for dependent_field in dependent_list:
                if not self.merged_document.get(dependent_field, '').strip():
                    self._error(field, '{0} can\'t have a value if {1} is empty'.format(field, dependent_field))


    def _validate_construction_before_inventory(self, check_const_inv_dts, field, value):
        """
        Check that construction_dt is not > inventory_dt if both exist.
        Note that since dates can be partial, it is assumed that partial construction dates start on first of the
        year or first of the month. Inventory dates are assumed to be on the last day of the year or month.
        In practice, we don't see partial inventory dates. We are doing just a string compare rather than
        translating to actual dates which works as long as the dates are valid.

        The rule's arguments are validated against this schema:
        {'type': 'boolean'}
         """
        if check_const_inv_dts:
            construction_date = self.merged_document.get('firstConstructionDate', '').strip()
            inventory_date = self.merged_document.get('siteEstablishmentDate', '').strip()
            if (construction_date and inventory_date) and (construction_date > inventory_date):
                self._error(field, "firstConstructionDate cannot be more recent than siteEstablishmnetDate")

    def _validate_check_well_hole_depths(self, check_well_hole_depths, field, value):
        """
        Check that well depth is not > hole depth when both are not empty

        The rule's arguments are validated against this schema:
        {'type': 'boolean'}
         """
        if check_well_hole_depths:
            try:
                hole_depth = float(self.merged_document.get('holeDepth', '').strip())
                well_depth = float(self.merged_document.get('wellDepth', '').strip())
            except ValueError:
                pass
            else:
                if (hole_depth and well_depth) and (well_depth > hole_depth):
                    self._error(field, "wellDepth cannot be greater than holeDepth")


    def _validate_check_valid_site_type_update(self, check_valid_update, field, value):
        """
        Check that if the field is changing from an existing site that it is in the allowed transitions

        The rule's arguments are validated against this schema
        {'type': 'boolean'}

        """
        if check_valid_update and self.update:
            stripped_value = value.strip()
            existing_value = self.existing_document.get(field, '')
            if stripped_value and existing_value:
                transitions = site_type_transition_reference.get_allowed_transitions(existing_value)
                if transitions and transitions.count(stripped_value) == 0:
                    self._error(field, 'Can not change a siteType with existing value {0} to {1}'.format(existing_value, stripped_value))

