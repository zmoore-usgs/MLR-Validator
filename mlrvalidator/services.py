
from flask import request
from flask_restplus import Api, Resource, fields
from werkzeug.exceptions import BadRequest

from app import application, error_validator, warning_validator

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
    "wellDepth": fields.String(),
})

location_model = api.clone('LocationModel', ddot_location_model, {
    "created": fields.String(),
    "createdBy": fields.String(),
    "decimalLatitude" : fields.Integer(),
    "decimalLongitude" : fields.Integer(),
    "id": fields.Integer(),
    "stationIx" : fields.Integer(),
    "updated": fields.String(),
    "updatedBy": fields.String(),
})

validate_location_model = api.model('ValidateLocationModel', {
    'ddotLocation' : fields.Nested(ddot_location_model),
    'existingLocation' : fields.Nested(location_model)
})

validation_model = api.model('SuccessModel', {'validation_passed_message': fields.String(),
                                              'warning_message': fields.String(),
                                              'fatal_error_message': fields.String()})

def _validate_response(req_json, update=False):
    if 'ddotLocation' not in req_json or 'existingLocation' not in req_json:
        raise BadRequest
    ddot_location = req_json.get('ddotLocation')
    existing_location = req_json.get('existingLocation')
    no_errors = error_validator.validate(ddot_location, existing_location, update=update)
    no_warnings = warning_validator.validate(ddot_location, existing_location)

    response = {}
    if not no_errors:
        response["fatal_error_message"] = 'Fatal Errors: {0}'.format(dict(error_validator.errors))
    if not no_warnings:
        response["warning_message"] = 'Validation Warnings: {0}'.format(dict(warning_validator.warnings))
    if no_errors and no_warnings:
        response["validation_passed_message"] = 'Validations Passed'

    return response, 200

@api.route('/validators/add')
class AddValidator(Resource):

    @api.response(200, 'Successfully validated', validation_model)
    @api.expect(validate_location_model)
    def post(self):
        return _validate_response(request.get_json())


@api.route('/validators/update')
class UpdateValidator(Resource):

    @api.response(200, 'Successfully validated', validation_model)
    @api.expect(validate_location_model)
    def post(self):
        return _validate_response(request.get_json(), update=True)

