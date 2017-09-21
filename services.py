from flask import request
from flask_restplus import Api, Resource, fields
from schema import get_insert_schema, get_warning_schema

from app import application, sitefile_validator, sitefile_warning_validator
from validator import ValidateError, validate as validate_data

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

success_model = api.model('SuccessModel', {'success_message': fields.String()})

error_model = api.model('ErrorModel', {
    'validation_error_message': fields.String()
})


@api.route('/validators')
class Validator(Resource):

    @api.response(200, 'Successfully validated', success_model)
    @api.response(400, 'File can not be validated', error_model)
    @api.expect(location_model)
    def post(self):
        data = request.get_json()
        schema = get_insert_schema()
        warning_schema = get_warning_schema()
        err_message = ""
        warn_message = ""
        try:
            result = validate_data(data, schema, sitefile_validator)
        except ValidateError as err:
            err_message = err.message
        try:
            result_warn = validate_data(data, warning_schema, sitefile_warning_validator)
        except ValidateError as warn:
            warn_message = warn.message

        status_object = {}
        if err_message:
            status_object['fatal_error_message'] = err_message
        if warn_message:
            status_object['warning_message'] = warn_message
        if result and result_warn:
            status_object['success_message'] = result

        response, status = {
                status_object
                }, 200

        return response, status
