
from app import application, sitefile_insert_error_validator, sitefile_insert_warning_validator
from .schema import schema_registry
from flask import request
from flask_restplus import Api, Resource, fields

api = Api(application,
          title='MLR Validator',
          description='Provides a service to take a json input of an MLR transaction, validate it, respond back with a response containing the validation results',
          default='Validator',
          default_label='Validator',
          doc='/api')

location_model = api.model('LocationModel', {
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
    "decimalLatitude": fields.String(),
    "decimalLongitude": fields.String(),
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
    "stationIx": fields.String(),
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

success_model = api.model('SuccessModel', {'message': fields.String()})

error_model = api.model('ErrorModel', {
    'fatal_error_message': fields.String()
})


@api.route('/validators')
class Validator(Resource):

    @api.response(200, 'Successfully validated', success_model)
    @api.expect(location_model)
    def post(self):
        data = request.get_json()
        insert_error_schema = schema_registry.get('insert_error_schema')
        insert_warning_schema = schema_registry.get('insert_warning_schema')
        error_result = sitefile_insert_error_validator.validate(data, insert_error_schema)
        warning_result = sitefile_insert_warning_validator.validate(data, insert_warning_schema)
        status_object = {}

        if not error_result:
            status_object["fatal_error_message"] = 'Fatal Errors: {0}'.format(sitefile_insert_error_validator.errors)
        if not warning_result:
            status_object["warning_message"] = 'Validation Warnings: {0}'.format(
                sitefile_insert_warning_validator.errors)
        if error_result and warning_result:
            status_object["validation_passed_message"] = 'Validations Passed'

        response, status = status_object, 200

        return response, status
