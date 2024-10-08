import pandas as pd
import numpy as np
import os
import json
import sys
from datetime import date
import seaborn as sns
import matplotlib.pyplot as plt
import xlsxwriter as xw

dir = os.getcwd()

### PATH NAMES ### 
data_path = os.path.join(dir,"data")
post_path = os.path.join(dir,'data','posts')
results_path = os.path.join(dir, 'results', 'results_json')
results_summary_path = os.path.join(dir, 'results', 'results_summary')
if not os.path.exists(results_summary_path):
    os.makedirs(results_summary_path)

# Summary excel file:
results_book = xw.Workbook(os.path.join(results_summary_path, "ASHP_Case_Studies.xlsx"))
result_sheet_all = results_book.add_worksheet('summary')

# Outputs to summarize:
output = ["Location", "Building Type", "Configuration", "ASHP-SH Size [ton]", "ASHP-WH Size [ton]", "LCC", "LCC-BAU", "NPV",
          "LCCC", "NPV-Fuel", "NPV-Elec Bill", "CO2 Emission Saving [kTonne]", "Avoided Health Damages [T$]", "Avoided Climate Damages [T$]",
          "ASHP-SH Annual Elec Consumption", "ASHP-WH Annual Elec Consumption", "ASHP-SH Annual Thermal Production-Heat", 
          "ASHP-SH Annual Thermal Production-Cool", "ASHP-WH Annual Thermal Production", "Electric Heater Size [mmbtu]",
          "Electric Heater Annual Thermal Production", "Electric Heater Annual Elec Consumption", 
          "Existing Chiller Annual Elec Consumption", "Existing Chiller Annual Cooling Production", 
          "Existing Boiler Annual Fuel Consumption", "Existing Boiler Annual Thermal Production", "Payback Years"]    


jsonfiles = os.listdir(results_path)

output_value_list = []
for scenario_json in jsonfiles:
    if scenario_json == ".DS_Store":
        continue

    scenario = scenario_json.split('.')[0]
    location = scenario.split('_')[0]
    building = scenario.split('_')[1]
    config = int(scenario.split('config')[1])

    #if config == 2 or config == 4:
    #    continue

    hours_to_graph_lower = 0
    hours_to_graph_higher = 48

    with open(os.path.join(results_path, scenario_json), 'rb') as handle:
        parsed_data = json.load(handle)

    ## Print outputs:
    output_ASHP_WH = parsed_data["ASHPWaterHeater"]
    output_ASHP_SH = parsed_data["ASHPSpaceHeater"]
    output_EB = parsed_data["ExistingBoiler"]
    output_Financial = parsed_data["Financial"]
    output_ELoad = parsed_data["ElectricLoad"]
    output_HLoad = parsed_data["HeatingLoad"]
    output_Site = parsed_data["Site"]

    try:
        output_EH = parsed_data["ElectricHeater"]
    except:
        output_EH = {}

    try:
        output_EC = parsed_data["ExistingChiller"]
    except:
        output_EC = {}    

    hour = list(range(8760))

    # ASHP-SP output:
    output_ASHP_SH_to_load_heating = output_ASHP_SH["thermal_to_space_heating_load_series_mmbtu_per_hour"]
    output_ASHP_SH_to_load_cooling = output_ASHP_SH["thermal_to_load_series_ton"]
    output_ASHP_SH_size = output_ASHP_SH["size_ton"]
    output_ASHP_SH_elec_consumption = output_ASHP_SH["annual_electric_consumption_kwh"]
    output_ASHP_SH_heating_production = output_ASHP_SH["annual_thermal_production_mmbtu"]
    output_ASHP_SH_cooling_production = output_ASHP_SH["annual_thermal_production_tonhour"]

    # ASHP-WH output:
    output_ASHP_WH_to_dwh_load_heating = output_ASHP_WH["thermal_to_dhw_load_series_mmbtu_per_hour"]
    output_ASHP_WH_size = output_ASHP_WH["size_ton"]
    output_ASHP_WH_elec_consumption = output_ASHP_WH["annual_electric_consumption_kwh"]
    output_ASHP_WH_heating_production = output_ASHP_WH["annual_thermal_production_mmbtu"]

    # Electric Heater output:
    try:
        output_EH_to_heating_load = output_EH["thermal_to_load_series_mmbtu_per_hour"]
        output_EH_size = output_EH["size_mmbtu_per_hour"]
        output_EH_elec_consumption = output_EH["annual_electric_consumption_kwh"]
        output_EH_heating_production = output_EH["annual_thermal_production_mmbtu"]
    except:
        output_EH_to_heating_load = [0] * 8760
        output_EH_size = 0
        output_EH_elec_consumption = 0
        output_EH_heating_production = 0

    # Existing Boiler output:
    try:
        output_EB_to_sh_load = output_EB["thermal_to_space_heating_load_series_mmbtu_per_hour"]
        output_EB_to_dwh_load = output_EB["thermal_to_dhw_load_series_mmbtu_per_hour"]
        output_EB_heating_production = output_EB["annual_thermal_production_mmbtu"]
        output_EB_fuel_consumption = output_EB["annual_fuel_consumption_mmbtu"]
    except:
        output_EB_to_sh_load = [0] * 8760
        output_EB_to_dwh_load = [0] * 8760
        output_EB_heating_production = 0
        output_EB_fuel_consumption = 0

    # Existing Chiller:
    try:
        output_EC_to_cooling_load = output_EC["thermal_to_load_series_ton"]
        output_EC_elec_consumption = output_EC["annual_electric_consumption_kwh"]
        output_EC_cooling_production = output_EC["annual_thermal_production_tonhour"]
    except:
        output_EC_to_cooling_load = [0] * 8760
        output_EC_elec_consumption = 0
        output_EC_cooling_production = 0

    # Emission Impacts:
    output_CO2_saving = output_Site["lifecycle_emissions_tonnes_CO2_bau"] -output_Site["lifecycle_emissions_tonnes_CO2"]
    avoided_health_damages = output_Financial["lifecycle_emissions_cost_health_bau"] - output_Financial["lifecycle_emissions_cost_health"]
    avoided_climate_damages = output_Financial["lifecycle_emissions_cost_climate_bau"] - output_Financial["lifecycle_emissions_cost_climate"]

    # Net Savings:
    lcc = output_Financial["lcc"]
    lcc_bau = output_Financial["lcc_bau"]
    npv = output_Financial["lcc_bau"] - output_Financial["lcc"]
    lccc = output_Financial["lifecycle_generation_tech_capital_costs"]
    npv_fuel = output_Financial["lifecycle_fuel_costs_after_tax_bau"]-output_Financial["lifecycle_fuel_costs_after_tax"]
    npv_elec_bill = output_Financial["lifecycle_elecbill_after_tax_bau"]-output_Financial["lifecycle_elecbill_after_tax"]
    
    # Payback Years:
    simple_payback_years = output_Financial["simple_payback_years"]

    output_value = [location, building, config, output_ASHP_SH_size, output_ASHP_WH_size, lcc, lcc_bau, npv,
          lccc, npv_fuel, npv_elec_bill, output_CO2_saving/1000, avoided_health_damages/1000, avoided_climate_damages/1000,
          output_ASHP_SH_elec_consumption, output_ASHP_WH_elec_consumption, output_ASHP_SH_heating_production, 
          output_ASHP_SH_cooling_production, output_ASHP_WH_heating_production, output_EH_size, output_EH_elec_consumption,
          output_EH_heating_production, output_EC_elec_consumption, output_EC_cooling_production, output_EB_fuel_consumption,
          output_EB_heating_production, simple_payback_years] 
    
    output_df = pd.DataFrame(output_value)
    output_df_T = output_df.T
    output_df_T.columns = output
    output_value_list += [output_df_T]

output_allscens = pd.concat(output_value_list, ignore_index=True, sort=False)

output_allscens.to_excel(os.path.join(results_summary_path,"ASHP_Case_Studies.xlsx"))


