import os
import json
#from pypvwatts import PVWatts
import glob

dir = os.getcwd()

post_path = os.path.join(dir,'data','posts')
files_posts = glob.glob(os.path.join(dir,'data','posts/*'))
files_results = glob.glob(os.path.join(dir,'results/results_json/*'))

for f in files_posts:
    os.remove(f)
for f in files_results:
    os.remove(f)    

### Locations:
locations = ['LosAngeles', 'Chicago', 'Minneapolis', 'Miami']  
#locations = ['LosAngeles']    

### Building types:
building_types = ['LargeOffice', 'LargeHotel', 'MidriseApartment', 'RetailStore', 'SecondarySchool']

### Configulations:
configs = ['config1', 'config2', 'config3', 'config4']

### Coupled technologies:
#coupled_techs = ['none', 'PVB', 'TES']
coupled_techs = ['TES']

### Min load factor of ASHP:
min_load_factor = 0.25

### For PVWatts API
pvwatts_api = 'E7us40wU4Qk9d0jhmsixpDLw1S99xhmUv1DTsjvu'

### Create posts:
def main():
    for location in locations:
        for building in building_types:
            for config in configs:
                for tech in coupled_techs:

                    ### Base post:
                    post = {}

                    # Site:
                    post['Site'] = {}
                    if location == 'LosAngeles':
                        post['Site']['latitude'] = 34.0549
                        post['Site']['longitude'] = -118.2426
                    elif location == 'Chicago':
                        post['Site']['latitude'] = 41.8781
                        post['Site']['longitude'] = -87.6298
                    elif location == 'Minneapolis':
                        post['Site']['latitude'] = 44.9778
                        post['Site']['longitude'] = -93.2650
                    elif location == 'Miami':
                        post['Site']['latitude'] = 25.7617
                        post['Site']['longitude'] = -80.1918

                    # Electric Load
                    post['ElectricLoad'] = {}
                    post['ElectricLoad']['city'] = location
                    post['ElectricLoad']['doe_reference_name'] = building

                    # Heating Load:
                    post['SpaceHeatingLoad'] = {}
                    post['SpaceHeatingLoad']['city'] = location
                    post['SpaceHeatingLoad']['doe_reference_name'] = building

                    post['DomesticHotWaterLoad'] = {}
                    post['DomesticHotWaterLoad']['city'] = location
                    post['DomesticHotWaterLoad']['doe_reference_name'] = building

                    post['CoolingLoad'] = {}
                    post['CoolingLoad']['city'] = location
                    post['CoolingLoad']['doe_reference_name'] = building

                    # Utility Rate:
                    post['ElectricTariff'] = {}

                    if location == 'LosAngeles':
                        post['ElectricTariff']['urdb_label'] = '5b5f6ad95457a37c63409a7b'
                    elif location == 'Chicago':
                        post['ElectricTariff']['urdb_label'] = '64c008292bb177188901afd2'
                    elif location == 'Minneapolis':
                        post['ElectricTariff']['urdb_label'] = '539fc46eec4f024c27d8c6ff'
                    elif location == 'Miami':
                        post['ElectricTariff']['urdb_label'] = '5cdeea305457a3897540c5d2'
                    
                    #############################################################################
                    ### Config 1:
                    ## Existing boiler can serve space heating and DHW load
                    ## ASHP-SH and ASHP-WH can be deployed to serve space heating and DWH load
                    ## ASHP-SH cannot serve cooling load
                    ## Existing chiller serves cooling load
                                       
                    if config == 'config1':
                        post1 = post.copy()

                        # ASHP:
                        post1['ASHPSpaceHeater'] = {}
                        post1['ASHPSpaceHeater']['can_serve_cooling'] = False
                        post1['ASHPSpaceHeater']['min_allowable_peak_capacity_fraction'] = min_load_factor

                        # ASHP Water Heater:
                        post1['ASHPWaterHeater'] = {}
                        
                        # Existing Boiler:
                        post1['ExistingBoiler'] = {}

                        if location == 'LosAngeles':
                            post1['ExistingBoiler']['fuel_cost_per_mmbtu'] = 14.8
                        elif location == 'Chicago':
                            post1['ExistingBoiler']['fuel_cost_per_mmbtu'] = 9.1
                        elif location == 'Minneapolis':
                            post1['ExistingBoiler']['fuel_cost_per_mmbtu'] = 8.7
                        elif location == 'Miami':
                            post1['ExistingBoiler']['fuel_cost_per_mmbtu'] = 10.8

                        post1['ExistingBoiler']['can_serve_dhw'] = True
                        post1['ExistingBoiler']['can_serve_space_heating'] = True

                        # Existing Chiller:
                        post1['ExistingChiller'] = {}

                        # PV + Battery:
                        if tech == 'PVB':
                            post1['PV'] = {}
                            post1['ElectricStorage'] = {}

                        # TES:    
                        elif tech == 'TES':
                            post1['HotThermalStorage'] = {}
                            post1['ColdThermalStorage'] = {}

                        post_final = post1

                    
                    #############################################################################
                    ### Config 2:
                    ## Existing boiler CANNOT serve space heating and DHW load
                    ## ASHP-SH is FORCED to be deployed to serve space heating load
                    ## ASHP-SH cannot serve cooling load
                    ## ASHP-WH is FORCED to be deployed to serve DHW load
                    ## Existing chiller serves cooling load
                    ## Electric Heater replaces Existing Boiler as backup system

                    if config == 'config2':

                        post2 = post.copy()
                        # ASHP-SH
                        post2['ASHPSpaceHeater'] = {}
                        post2['ASHPSpaceHeater']['force_into_system'] = True
                        post2['ASHPSpaceHeater']['can_serve_cooling'] = False
                        post2['ASHPSpaceHeater']['min_allowable_peak_capacity_fraction'] = min_load_factor
                        #post2['ASHPSpaceHeater']['heating_cf'] = [1]*8760
                        #post2['ASHPSpaceHeater']['heating_cop'] = [1]*8760

                        # ASHP-WH
                        post2['ASHPWaterHeater'] = {}
                        post2['ASHPWaterHeater']['force_into_system'] = True
                        #post2['ASHPWaterHeater']['heating_cf'] = [1]*8760
                        #post2['ASHPWaterHeater']['heating_cop'] = [1]*8760

                        # Existing Boiler
                        post2['ExistingBoiler'] = {}

                        if location == 'LosAngeles':
                            post2['ExistingBoiler']['fuel_cost_per_mmbtu'] = 14.8
                        elif location == 'Chicago':
                            post2['ExistingBoiler']['fuel_cost_per_mmbtu'] = 9.1
                        elif location == 'Minneapolis':
                            post2['ExistingBoiler']['fuel_cost_per_mmbtu'] = 8.7
                        elif location == 'Miami':
                            post2['ExistingBoiler']['fuel_cost_per_mmbtu'] = 10.8

                        #post2['ExistingBoiler']['can_serve_space_heating'] = False
                        #post2['ExistingBoiler']['can_serve_dhw'] = False

                        # Electric Heater:
                        #post2['ElectricHeater'] = {}
                        #post2['ElectricHeater']['max_mmbtu_per_hour'] = 99999999

                        # Existing Chiller:
                        post2['ExistingChiller'] = {}

                        # PV + Battery:
                        if tech == 'PVB':
                            post2['PV'] = {}
                            post2['ElectricStorage'] = {}

                        # TES:    
                        elif tech == 'TES':
                            post2['HotThermalStorage'] = {}
                            post2['ColdThermalStorage'] = {}

                        post_final = post2
                        

                    #############################################################################
                    ### Config 3:
                    ## Existing boiler CAN serve space heating and DHW load
                    ## ASHP-SH can be deployed to serve space heating load AND COOLING Load
                    ## ASHP-WH can be deployed to serve DHW load
                    ## Existing chiller can also cooling load along with ASHP-SP

                    if config == 'config3':

                        post3 = post.copy()

                        # ASHP-SH
                        post3['ASHPSpaceHeater'] = {}
                        post3['ASHPSpaceHeater']['min_allowable_peak_capacity_fraction'] = min_load_factor

                        # ASHP Water Heater:
                        post3['ASHPWaterHeater'] = {}

                        # Existing Boiler
                        post3['ExistingBoiler'] = {}
                        #post3['ExistingBoiler']['can_serve_space_heating'] = True
                        #post3['ExistingBoiler']['can_serve_dhw'] = True

                        if location == 'LosAngeles':
                            post3['ExistingBoiler']['fuel_cost_per_mmbtu'] = 14.8
                        elif location == 'Chicago':
                            post3['ExistingBoiler']['fuel_cost_per_mmbtu'] = 9.1
                        elif location == 'Minneapolis':
                            post3['ExistingBoiler']['fuel_cost_per_mmbtu'] = 8.7
                        elif location == 'Miami':
                            post3['ExistingBoiler']['fuel_cost_per_mmbtu'] = 10.8

                        # Existing Chiller:
                        post3['ExistingChiller'] = {}  

                        # PV + Battery:
                        if tech == 'PVB':
                            post3['PV'] = {}
                            post3['ElectricStorage'] = {}

                        # TES:    
                        elif tech == 'TES':
                            post3['HotThermalStorage'] = {}
                            post3['ColdThermalStorage'] = {}  

                        post_final = post3


                    #############################################################################
                    ### Config 4:
                    ## Existing boiler CANNOT serve space heating and DHW load
                    ## ASHP-SH IS FORCED to be deployed to serve space heating load AND COOLING Load
                    ## ASHP-SH IS FORCED to serve cooling load
                    ## ASHP-WH IS FORCED to deployed to serve DHW load
                    ## Existing chiller CANNOT serve cooling load along with ASHP-SP
                    ## Electric Heater replaces existing boiler as backup for spacing

                    if config == 'config4':

                        post4 = post.copy()

                        # ASHP-SH
                        post4['ASHPSpaceHeater'] = {}
                        post4['ASHPSpaceHeater']['can_serve_cooling'] = True
                        post4['ASHPSpaceHeater']['force_into_system'] = True
                        post4['ASHPSpaceHeater']['min_allowable_peak_capacity_fraction'] = min_load_factor

                        # ASHP-WH
                        post4['ASHPWaterHeater'] = {}
                        post4['ASHPWaterHeater']['force_into_system'] = True

                        # Existing Boiler
                        post4['ExistingBoiler'] = {}
                        #post4['ExistingBoiler']['can_serve_space_heating'] = False
                        #post4['ExistingBoiler']['can_serve_dhw'] = False

                        if location == 'LosAngeles':
                            post4['ExistingBoiler']['fuel_cost_per_mmbtu'] = 14.8
                        elif location == 'Chicago':
                            post4['ExistingBoiler']['fuel_cost_per_mmbtu'] = 9.1
                        elif location == 'Minneapolis':
                            post4['ExistingBoiler']['fuel_cost_per_mmbtu'] = 8.7
                        elif location == 'Miami':
                            post4['ExistingBoiler']['fuel_cost_per_mmbtu'] = 10.8


                        # PV + Battery:
                        if tech == 'PVB':
                            post4['PV'] = {}
                            post4['ElectricStorage'] = {}

                        # TES:    
                        elif tech == 'TES':
                            post4['HotThermalStorage'] = {}
                            post4['ColdThermalStorage'] = {}  

                        post_final = post4

                    if tech == 'none':
                        scenario_name = location+'_'+building+'_'+config
                    else:
                        scenario_name = location+'_'+building+'_'+config+'_'+tech
                    with open(os.path.join(post_path, scenario_name + '.json'), 'w') as handle:
                        json.dump(post_final, handle)  
                 
main()
