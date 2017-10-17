from . import site_type_cross_field_reference
from .base_cross_field_validator import BaseCrossFieldValidator


class SiteTypeCrossFieldValidator(BaseCrossFieldValidator):

    def _validator_site_type_field(self, field, value):
        """
        Check the site type field dependency for this field using the current site type value. If
        the field is in the notNullAttrs than it can't be empty/null. If the field is in nullAttrs it must be empty/null
        """
        site_type_value = self.merged_document.get('siteTypeCode', '').strip()
        field_value = value.strip()
        ref_for_site_type = site_type_cross_field_reference.get_site_type_field_dependencies(site_type_value)
        if (ref_for_site_type.get('notNullAttrs').count(field) == 1) and not field_value:
            self._error(field, 'Site type {0} requires that {1} field be present.'.format(site_type_value, field))

        if (ref_for_site_type.get('nullAttrs').count(field) == 1) and field_value:
            self._error(field, '{0} must be empty for the site type {1}'.format(field, value))


    def _validator_all_site_type_fields(self, field, value):
        """
        # Check that for a given site type all the not nullable fields are not null
        # and that all nullable fields are null

        """
        stripped_value = value.strip()
        if stripped_value:
            site_type_ref = site_type_cross_field_reference.get_site_type_field_dependencies(value)
            not_null_attrs = site_type_ref['notNullAttrs']
            null_attrs = site_type_ref['nullAttrs']
            nn_attr_field_problems = []
            n_attr_field_problems = []
            for nn_attr in not_null_attrs:
                try:
                    nn_attr_field_val = self.merged_document[nn_attr].strip()
                except KeyError:
                    nn_attr_field_problems.append(nn_attr)
                else:
                    if len(nn_attr_field_val) == 0:
                        nn_attr_field_problems.append(nn_attr)
            for n_attr in null_attrs:
                try:
                    n_attr_field_val = self.merged_document[n_attr].strip()
                except KeyError:
                    continue
                else:
                    if len(n_attr_field_val) != 0:
                        n_attr_field_problems.append(n_attr)
            if len(nn_attr_field_problems) > 0 or len(n_attr_field_problems) > 0:
                nn_attrs = ', '.join(nn_attr_field_problems)
                n_attrs = ', '.join(n_attr_field_problems)
                error_message = 'Field errors for siteTypeCode: {}.'.format(value)
                if len(nn_attr_field_problems) > 0:
                    error_message += ' The following fields must not be null: {}.'.format(nn_attrs)
                if len(n_attr_field_problems) > 0:
                    error_message += ' The following fields must be null: {}.'.format(n_attrs)
                return self._error(field, error_message)


