import pandas as pd
import numpy as np
import os
import json
import sys
from datetime import date
#import seaborn as sns
import matplotlib.pyplot as plt
import xlsxwriter as xw

dir = os.getcwd()

### PATH NAMES ### 
data_path = os.path.join(dir,"data")
post_path = os.path.join(dir,'data','posts')
results_path = os.path.join(dir, 'results', 'results_json')

jsonfiles = os.listdir(results_path)

output_value_list = []
for scenario_json in jsonfiles:
    if scenario_json == ".DS_Store":
        continue
    
    scenario = scenario_json.split('.')[0]
    location = scenario.split('_')[0]
    building = scenario.split('_')[1]
    config = int(scenario.split('config')[1])

    hours_to_graph_lower = 0
    hours_to_graph_higher = 200

    hours_to_graph_lower_cooling = 4800
    hours_to_graph_higher_cooling = 5000

    with open(os.path.join(results_path, scenario_json), 'rb') as handle:
        parsed_data = json.load(handle)


    output_ASHP_WH = parsed_data["ASHPWaterHeater"]
    output_ASHP_SH = parsed_data["ASHPSpaceHeater"]
    output_EB = parsed_data["ExistingBoiler"]
    output_Financial = parsed_data["Financial"]
    output_ELoad = parsed_data["ElectricLoad"]
    output_HLoad = parsed_data["HeatingLoad"]
    output_CLoad = parsed_data["CoolingLoad"]
    output_Site = parsed_data["Site"]
    hour = list(range(8760))

    try:
        output_EH = parsed_data["ElectricHeater"]
    except:
        output_EH = {}

    try:
        output_EC = parsed_data["ExistingChiller"]
    except:
        output_EC = {} 

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
        output_EB_heating_production = [0]
        output_EB_fuel_consumption = [0]

    # Existing Chiller:
    try:
        output_EC_to_cooling_load = output_EC["thermal_to_load_series_ton"]
        output_EC_elec_consumption = output_EC["annual_electric_consumption_kwh"]
        output_EC_cooling_production = output_EC["annual_thermal_production_tonhour"]
    except:
        output_EC_to_cooling_load = [0] * 8760
        output_EC_elec_consumption = 0
        output_EC_cooling_production = 0

    # Heating Load
    output_SHLoad = output_HLoad["space_heating_thermal_load_series_mmbtu_per_hour"]
    output_DWHLoad = output_HLoad["dhw_thermal_load_series_mmbtu_per_hour"]
    output_SCLoad = output_CLoad["load_series_ton"]

    ## Figures
    # Heating Load Supply:
    dict_hload = {'hour': hour, 'ASHP-SH to SH Load': output_ASHP_SH_to_load_heating, 'Existing Boiler to SH Load': output_EB_to_sh_load} 
    
    # DWH Supply:
    dict_dhwload = {'hour': hour, 'ASHP-WH to DHW Load': output_ASHP_WH_to_dwh_load_heating, 'ExistingBoiler to DHW Load': output_EB_to_dwh_load}    

    # Graph performance data - Space Heating
    #plt.style.use("seaborn")
    #colors = sns.color_palette("Pastel1", 6)
    colors = ["#a8e6cf", "#ffaaa5"]
    #sns.set_style(style='white')
    labels=["ASHP-SH to SH Load", "Existing Boiler to SH Load"]

    fig, ax = plt.subplots(figsize=(17,5))
    plt.stackplot(hour[hours_to_graph_lower:hours_to_graph_higher], output_ASHP_SH_to_load_heating[hours_to_graph_lower:hours_to_graph_higher], 
                output_EB_to_sh_load[hours_to_graph_lower:hours_to_graph_higher],
                labels=labels, colors=colors, edgecolor = "none")
    plt.plot(hour[hours_to_graph_lower:hours_to_graph_higher], output_SHLoad[hours_to_graph_lower:hours_to_graph_higher], label = "SH Load",linewidth=1, color='black')
    plt.xlabel("Hour in Year",fontsize=17)
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    plt.ylabel("MMBTU", fontsize=15)
    plt.rcParams["axes.edgecolor"] = "black"
    plt.rcParams["axes.linewidth"] = 1
    plt.legend(bbox_to_anchor=(1.0, 1.0), loc='upper left')
    plt.xlim(hours_to_graph_lower,hours_to_graph_higher)

    fig.savefig(os.path.join(dir, 'results', 'figures', 'ashp_sh_'+scenario+'.png'), dpi=300,bbox_inches='tight')


    # Graph performance data - DHW Heating
    #plt.style.use("seaborn")
    #colors = sns.color_palette("Pastel1", 6)
    colors = ["#a8e6cf", "#ffaaa5"]
    #sns.set_style(style='white')
    labels=["ASHP-WH to DHW Load", "Existing Boiler to DHW Load"]

    fig, ax = plt.subplots(figsize=(17,5))
    plt.stackplot(hour[hours_to_graph_lower:hours_to_graph_higher], output_ASHP_WH_to_dwh_load_heating[hours_to_graph_lower:hours_to_graph_higher], 
                output_EB_to_dwh_load[hours_to_graph_lower:hours_to_graph_higher],labels=labels, colors=colors, edgecolor = "none")
    plt.plot(hour[hours_to_graph_lower:hours_to_graph_higher], output_DWHLoad[hours_to_graph_lower:hours_to_graph_higher], label = "DHW Load",linewidth=1, color='black')
    plt.xlabel("Hour in Year",fontsize=17)
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    plt.ylabel("MMBTU", fontsize=15)
    plt.rcParams["axes.edgecolor"] = "black"
    plt.rcParams["axes.linewidth"] = 1
    plt.legend(bbox_to_anchor=(1.0, 1.0), loc='upper left')
    plt.xlim(hours_to_graph_lower,hours_to_graph_higher)

    fig.savefig(os.path.join(dir, 'results', 'figures', 'ashp_wh_'+scenario+'.png'), dpi=300,bbox_inches='tight')

    # Space Cooling:
    #plt.style.use("seaborn")
    #colors = sns.color_palette("Pastel1", 6)
    colors = ["#a8e6cf", "#ffaaa5"]
    #sns.set_style(style='white')
    labels=["ASHP-SH to SC Load", "Existing Chiller to SC Load"]

    fig, ax = plt.subplots(figsize=(17,5))
    plt.stackplot(hour[hours_to_graph_lower_cooling:hours_to_graph_higher_cooling], output_ASHP_SH_to_load_cooling[hours_to_graph_lower_cooling:hours_to_graph_higher_cooling], 
                output_EC_to_cooling_load[hours_to_graph_lower_cooling:hours_to_graph_higher_cooling],labels=labels, colors=colors, edgecolor = "none")
    plt.plot(hour[hours_to_graph_lower_cooling:hours_to_graph_higher_cooling], output_SCLoad[hours_to_graph_lower_cooling:hours_to_graph_higher_cooling], label = "SC Load",linewidth=1, color='black')
    plt.xlabel("Hour in Year",fontsize=17)
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    plt.ylabel("Ton", fontsize=15)
    plt.rcParams["axes.edgecolor"] = "black"
    plt.rcParams["axes.linewidth"] = 1
    plt.legend(bbox_to_anchor=(1.0, 1.0), loc='upper left')
    plt.xlim(hours_to_graph_lower_cooling,hours_to_graph_higher_cooling)

    fig.savefig(os.path.join(dir, 'results', 'figures', 'ashp_sc_'+scenario+'.png'), dpi=300,bbox_inches='tight')
