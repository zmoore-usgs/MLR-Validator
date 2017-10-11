
from flask import request
from flask_restplus import Api, Resource, fields
from itertools import chain
from collections import defaultdict

from app import application, sitefile_single_field_validator, sitefile_warning_validator, sitefile_reference_validator

api = Api(application,
          title='MLR Validator',
          description='Provides a service to take a json input of an MLR transaction, validate it, respond back with a response containing the validation results',
          default='Validator',
          default_label='Validator',
          doc='/api')

ddot_location_model = api.model('DdotLocationModel', {
    "agencyCode": fields.String(),
    "agencyUseCode": fields.String(),
    "altitude": fields.String(),
    "altitudeAccuracyValue": fields.String(),
    "altitudeDatumCode": fields.String(),
    "altitudeMethodCode": fields.String(),
    "aquiferCode": fields.String(),
    "aquiferTypeCode": fields.String(),
    "basinCode": fields.String(),
    "contributingDrainageArea": fields.String(),
    "coordinateAccuracyCode": fields.String(),
    "coordinateDatumCode": fields.String(),
    "coordinateMethodCode": fields.String(),
    "countryCode": fields.String(),
    "countyCode": fields.String(),
    "created": fields.String(),
    "createdBy": fields.String(),
    "dataReliabilityCode": fields.String(),
    "dataTypesCode": fields.String(),
    "daylightSavingsTimeFlag": fields.String(),
    "districtCode": fields.String(),
    "drainageArea": fields.String(),
    "firstConstructionDate": fields.String(),
    "gwFileCode": fields.String(),
    "holeDepth": fields.String(),
    "hydrologicUnitCode": fields.String(),
    "instrumentsCode": fields.String(),
    "landNet": fields.String(),
    "latitude": fields.String(),
    "longitude": fields.String(),
    "mapName": fields.String(),
    "mapScale": fields.String(),
    "minorCivilDivisionCode": fields.String(),
    "nationalAquiferCode": fields.String(),
    "nationalWaterUseCode": fields.String(),
    "primaryUseOfSite": fields.String(),
    "primaryUseOfWaterCode": fields.String(),
    "projectNumber": fields.String(),
    "remarks": fields.String(),
    "secondaryUseOfSite": fields.String(),
    "secondaryUseOfWaterCode": fields.String(),
    "siteEstablishmentDate": fields.String(),
    "siteNumber": fields.String(),
    "siteTypeCode": fields.String(),
    "siteWebReadyCode": fields.String(),
    "sourceOfDepthCode": fields.String(),
    "stateFipsCode": fields.String(),
    "stationName": fields.String(),
    "tertiaryUseOfSiteCode": fields.String(),
    "tertiaryUseOfWaterCode": fields.String(),
    "timeZoneCode": fields.String(),
    "topographicCode": fields.String(),
    "updated": fields.String(),
    "updatedBy": fields.String(),
    "wellDepth": fields.String(),
    "transactionType": fields.String()
})

location_model = api.clone('LocationModel', ddot_location_model, {
    "decimalLatitude" : fields.Integer(),
    "decimalLongitude" : fields.Integer(),
    "id": fields.Integer(),
    "stationIx" : fields.Integer()
})

validate_location_model = api.model('ValidateLocationModel', {
    'ddotLocation' : fields.Nested(ddot_location_model),
    'existingLocation' : fields.Nested(location_model)
})

validation_model = api.model('SuccessModel', {'validation_passed_message': fields.String(),
                                              'warning_message': fields.String(),
                                              'fatal_error_message': fields.String()})


@api.route('/validators/add')
class AddValidator(Resource):

    @api.response(200, 'Successfully validated', validation_model)
    @api.expect(validate_location_model)
    def post(self):
        ddotLocation = request.get_json().get('ddotLocation')

        no_single_field_errors = sitefile_single_field_validator.validate(ddotLocation)
        no_reference_errors = sitefile_reference_validator.validate(ddotLocation)
        no_warnings = sitefile_warning_validator.validate(ddotLocation)

        status_object = {}
        if not (no_reference_errors and no_single_field_errors):
            single_field_errors = sitefile_single_field_validator.errors
            reference_errors = sitefile_reference_validator.errors
            all_errors = defaultdict(list)
            # This part combines all types errors for each field
            for k, v in chain(single_field_errors.items(), reference_errors.items()):
                all_errors[k].extend(v)
            status_object["fatal_error_message"] = 'Fatal Errors: {0}'.format(dict(all_errors))

        if not no_warnings:
            status_object["warning_message"] = 'Validation Warnings: {0}'.format(
                sitefile_warning_validator.errors)

        if no_single_field_errors and no_reference_errors and no_warnings:
            status_object["validation_passed_message"] = 'Validations Passed'

        return status_object, 200


@api.route('/validators/update')
class UpdateValidator(Resource):

    @api.response(200, 'Successfully validated', validation_model)
    @api.expect(validate_location_model)
    def post(self):
        ddotLocation = request.get_json().get('ddotLocation')
        existingLocation = request.get_json().get('existingLocation')

        no_single_field_errors = sitefile_single_field_validator.validate(ddotLocation, update=True)

        status_object = {}
        if not no_single_field_errors:
            status_object['fatal_error_message'] = 'Fatal Errors: {0}'.format(sitefile_single_field_validator.errors)

        if no_single_field_errors:
            status_object['validation_passed_message'] = 'Validations Passed'

        return status_object, 200

