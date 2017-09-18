import yaml


def get_insert_schema():

    raw_schema_yaml = """
        agencyCode:
            is_empty: False
            maxlength: 5
        siteNumber:
            maxlength: 15
            is_empty: False
        stationName:
            maxlength: 50
            is_empty: False
            valid_special_chars: True
        siteTypeCode:
            is_empty: False
            maxlength: 7
        latitude:
            maxlength: 11
            valid_latitude_dms: True
        longitude:
            maxlength: 12
            valid_longitude_dms: True
        coordinateAccuracyCode: 
            maxlength: 1
        coordinateDatumCode:
            maxlength: 10
        coordinateMethodCode:
            maxlength: 1
        altitude:
            type: numeric
            maxlength: 8
            valid_precision: True
        altitudeDatumCode:
            maxlength: 10
        altitudeMethodCode:
            maxlength: 1
        altitudeAccuracyValue:
            type: numeric
            maxlength: 3
        districtCode:
            is_empty: False
            maxlength: 3
        countryCode:
            is_empty: False
            maxlength: 2
        stateFipsCode:
            is_empty: False
            maxlength: 2
        countyCode:
            is_empty: False
            maxlength: 3
        minorCivilDivisionCode:
            maxlength: 5
        hydrologicUnitCode:
            maxlength: 16
        basinCode:
            maxlength: 2
        nationalAquiferCode:
            maxlength: 10
        aquiferCode:
            maxlength: 8
        aquiferTypeCode:
            maxlength: 1
        agencyUseCode:
            maxlength: 1
        dataReliabilityCode:
            maxlength: 1
        landNet:
            maxlength: 23
            valid_land_net: True
        mapName:
            maxlength: 20
        mapScale:
            maxlength: 7
            valid_map_scale_chars: True
        nationalWaterUseCode:
            maxlength: 2
        primaryUseOfSite:
            maxlength: 1
        secondaryUseOfSite:
            maxlength: 1
        tertiaryUseOfSiteCode:
            maxlength: 1
        primaryUseOfWaterCode:
            maxlength: 1
        secondaryUseOfWaterCode:
            maxlength: 1
        tertiaryUseOfWaterCode:
            maxlength: 1
        topographicCode:
            maxlength: 1
        dataTypesCode:
            maxlength: 30
            valid_data_types_chars: True
        instrumentsCode:
            maxlength: 30
            valid_instruments_chars: True
        contributingDrainageArea:
            type: positive_numeric
            maxlength: 8
        drainageArea:
            type: positive_numeric
            maxlength: 8
        firstConstructionDate:
            maxlength: 8
            valid_date: True
        siteEstablishmentDate:
            maxlength: 8
            valid_date: True
        holeDepth:
            type: numeric
            maxlength: 8
        wellDepth:
            type: numeric
            maxlength: 8
            valid_precision: True
        sourceOfDepthCode:
            maxlength: 1
        projectNumber:
            maxlength: 12
        timeZoneCode:
            is_empty: False
            maxlength: 5
        daylightSavingsTimeFlag:
            is_empty: False
            maxlength: 1
            allowed: [Y,N]
        remarks:
            maxlength: 50
        siteWebReadyCode:
            maxlength: 1
        gwFileCode:
            maxlength: 20
"""

    schema = yaml.load(raw_schema_yaml)
    return schema
