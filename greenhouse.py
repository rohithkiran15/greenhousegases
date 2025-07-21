import pandas as pd

data = pd.read_csv('greenhouse_gas_inventory_data_data.csv')

reshaped_data = data.pivot_table(
    index=['country_or_area', 'year'],
    columns='category',
    values='value'
).reset_index()

reshaped_data.columns.name = None

column_renames = {
    'carbon_dioxide_co2_emissions_without_land_use_land_use_change_and_forestry_lulucf_in_kilotonne_co2_equivalent': 'co2',
    'methane_ch4_emissions_without_land_use_land_use_change_and_forestry_lulucf_in_kilotonne_co2_equivalent': 'ch4',
    'nitrous_oxide_n2o_emissions_without_land_use_land_use_change_and_forestry_lulucf_in_kilotonne_co2_equivalent': 'n2o',
    'hydrofluorocarbons_hfcs_emissions_in_kilotonne_co2_equivalent': 'hfc',
    'perfluorocarbons_pfcs_emissions_in_kilotonne_co2_equivalent': 'pfc',
    'sulphur_hexafluoride_sf6_emissions_in_kilotonne_co2_equivalent': 'sf6',
    'nitrogen_trifluoride_nf3_emissions_in_kilotonne_co2_equivalent': 'nf3',
    'unspecified_mix_of_hydrofluorocarbons_hfcs_and_perfluorocarbons_pfcs_emissions_in_kilotonne_co2_equivalent': 'other_f_gases',
    'greenhouse_gas_ghgs_emissions_without_land_use_land_use_change_and_forestry_lulucf_in_kilotonne_co2_equivalent': 'total_ghg',
    'greenhouse_gas_ghgs_emissions_including_indirect_co2_without_lulucf_in_kilotonne_co2_equivalent': 'total_ghg_including_indirect_co2',
}

reshaped_data.rename(columns=column_renames, inplace=True)
reshaped_data.to_csv('reshaped_ghg_dataset.csv', index=False)

data = data.dropna()
data["year"] = data["year"].astype(int)
data["value"] = pd.to_numeric(data["value"], errors="coerce")
data = data.drop_duplicates()
data.to_csv("cleaned_greenhouse_data.csv", index=False)
