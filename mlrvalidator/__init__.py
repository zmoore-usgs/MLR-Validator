from mlrvalidator.reference import Aquifers, Counties, Hucs, Mcds, NationalAquifers, NationalWaterUseCodes, \
    ReferenceInfo, States

aquifer_reference = Aquifers('references/aquifer.json')
huc_reference = Hucs('references/huc.json')
mcd_reference = Mcds('references/mcd.json')
national_aquifer_reference = NationalAquifers('references/national_aquifer.json')
national_water_use_reference = NationalWaterUseCodes('references/national_water_use.json')
reference_lists = ReferenceInfo('references/reference_lists.json')
county_reference = Counties('references/county.json')
state_reference = States('references/state.json')