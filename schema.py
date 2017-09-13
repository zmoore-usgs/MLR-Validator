def get_insert_schema():
    schema = {
        'agencyCode': {
            'empty': False
        },
        'siteNumber': {
            'maxlength': 15,
            'empty': False
        },
        'stationName': {
            'maxlength': 50,
            'empty': False,
            'valid_chars': True
        },
        'siteTypeCode': {
            'empty': False
        },
        'decimalLatitude': {

        },
        'decimalLongitude': {

        },
        'latitude': {
            'valid_dms': True
        },
        'longitude': {

        },
        'coordinateAccuracyCode': {

        },
        'coordinateDatumCode': {

        },
        'coordinateMethodCode': {

        },
        'altitude': {
            'type': 'numeric'
        },
        'altitudeDatumCode': {

        },
        'altitudeMethodCode': {

        },
        'altitudeAccuracyValue': {
            'type': 'numeric',
            'maxlength': 3
        },
        'districtCode': {
            'empty': False
        },
        'countryCode': {
            'empty': False
        },
        'stateFipsCode': {
            'empty': False
        },
        'countyCode': {
            'empty': False
        },
        'minorCivilDivisionCode': {

        },
        'hydrologicUnitCode': {

        },
        'basinCode': {

        },
        'nationalAquiferCode': {

        },
        'aquiferCode': {

        },
        'aquiferTypeCode': {

        },
        'agencyUseCode': {

        },
        'dataReliabilityCode': {

        },
        'landNet': {
            'maxlength': 23,
            'valid_chars': True
        },
        'mapName': {
            'maxlength': 20
        },
        'mapScale': {
            'maxlength': 7
        },
        'nationalWaterUseCode': {

        },
        'primaryUseOfSite': {

        },
        'secondaryUseOfSite': {

        },
        'tertiaryUseOfSiteCode': {

        },
        'primaryUseOfWaterCode': {

        },
        'secondaryUseOfWaterCode': {

        },
        'tertiaryUseOfWaterCode': {

        },
        'topographicCode': {

        },
        'dataTypesCode': {
            'maxlength': 30,
            'valid_chars': True
        },
        'instrumentsCode': {
            'maxlength': 30,
            'valid_chars': True
        },
        'contributingDrainageArea': {
            'type': 'positive_numeric',
            'maxlength': 8
        },
        'drainageArea': {
            'type': 'positive_numeric',
            'maxlength': 8
        },
        'firstConstructionDate': {

        },
        'siteEstablishmentDate': {

        },
        'holeDepth': {
            'type': 'numeric'
        },
        'wellDepth': {
            'type': 'numeric'
        },
        'sourceOfDepthCode': {

        },
        'projectNumber': {
            'maxlength': 12
        },
        'timeZoneCode': {
            'empty': True
        },
        'daylightSavingsTimeFlag': {
            'empty': True
        },
        'remarks': {
            'maxlength': 50
        },
        'siteWebReadyCode': {

        },
        'gwFileCode': {

        },
        'created': {

        },
        'createdBy': {

        },
        'updated': {

        },
        'updatedBy': {

        },
    }

    return schema
