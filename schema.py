import yaml


def get_insert_schema():

    raw_schema_yaml = """
        agencyCode:
            empty: False
        siteNumber:
            maxlength: 15
            empty: False
        stationName:
            maxlength: 50
            empty: False
            valid_chars: True
        siteTypeCode:
            empty: False
        latitude:
            valid_dms: True
        longitude:
            valid_dms: True
        altitude:
            type: numeric
        altitudeAccuracyValue:
            type: numeric
            maxlength: 3
        districtCode:
            empty: False
        countryCode:
            empty: False
        stateFipsCode:
            empty: False
        countyCode:
            empty: False
        landNet:
            maxlength: 23
            valid_chars: True
        mapName:
            maxlength: 20
        mapScale:
            maxlength: 7
        dataTypesCode:
            maxlength: 30
            valid_chars: True
        instrumentsCode:
            maxlength: 30
            valid_chars: True
        contributingDrainageArea:
            type: positive_numeric
            maxlength: 8
        drainageArea:
            type: positive_numeric
            maxlength: 8
        holeDepth:
            type: numeric
        wellDepth:
            type: numeric
        projectNumber:
            maxlength: 12
        timeZoneCode:
            empty: True
        daylightSavingsTimeFlag:
            empty: True
        remarks:
            maxlength: 50
"""

    schema = yaml.load(raw_schema_yaml)
    return schema
