import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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

plt.figure(figsize=(18, 6))
ghg_by_country = reshaped_data.groupby('country_or_area')['total_ghg'].sum().sort_values(ascending=False)
ghg_by_country.plot(kind='line', marker='o')
plt.title('Total GHG Emissions by Country')
plt.xlabel('Country')
plt.ylabel('Total GHG Emissions')
plt.xticks(ticks=range(len(ghg_by_country.index)), labels=ghg_by_country.index, rotation=90)
plt.tight_layout()
plt.savefig('total_ghg_vs_country.png')
plt.close()


plt.figure(figsize=(12, 6))
ghg_by_year = reshaped_data.groupby('year')['total_ghg'].sum()
ghg_by_year.plot(kind='line', marker='o', color='green')
plt.title('Total GHG Emissions Over Years')
plt.xlabel('Year')
plt.ylabel('Total GHG Emissions')
plt.tight_layout()
plt.savefig('total_ghg_by_year.png')
plt.close()

gas_columns = ['co2', 'ch4', 'n2o', 'hfc', 'pfc', 'sf6', 'nf3', 'other_f_gases']
gas_sums = reshaped_data[gas_columns].sum()

plt.figure(figsize=(8, 8))
plt.pie(gas_sums, labels=None, autopct='%1.1f%%', startangle=140)
plt.title('Greenhouse Gas Contributions')
plt.axis('equal')
plt.legend(gas_columns, loc='center left', bbox_to_anchor=(1, 0.5), title="Gases")
plt.tight_layout()
plt.savefig('ghg_contributions_pie_chart.png')
plt.close()

plt.figure(figsize=(10, 6))
correlation = reshaped_data[gas_columns + ['total_ghg']].corr()
sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Heatmap of GHG Emissions')
plt.tight_layout()
plt.savefig('ghg_correlation_heatmap.png')
plt.close()