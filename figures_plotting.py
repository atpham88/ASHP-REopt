import pandas as pd
import numpy as np
import os
import altair as alt
from datetime import date
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt


# For debugging:
#run_with_ghp = 0

dir = os.getcwd()

## NET SAVINGS PLOT
file = "ASHP_Case_Studies.xlsx"
em_data = pd.read_excel(os.path.join(dir, "results", "results_summary", file))

# DATAFRAME PREPROCESSING
em_data = em_data.rename(columns={'NPV':'Value', 'NPV-Fuel':'Fuel Cost Savings'})
em_data = em_data[em_data['Configuration']==4]

df = em_data[['Location', 'Value', 'Fuel Cost Savings', 'NPV-Elec Bill', 'LCCC', 'Cost per ton', 'Building Type', 'Avoided Health Damages [T$]', 
              'CO2 Emission Saving [kTonne]', 'ASHP-SH Size [ton]', 'ASHP-WH Size [ton]', 'Bill Increase']]
df['Value'] = -df['Value']/1000
df['Fuel Cost Savings'] = df['Fuel Cost Savings']/1000
df['NPV-Elec Bill'] = -df['NPV-Elec Bill']/1000
df['LCCC'] = df['LCCC']/1000
df['Bill Increase'] = df['Bill Increase']/1000
df['Cost per ton'] = -df['Cost per ton']

#   Add respective policy labels to dataframe
df['climate'] = ''
df.loc[df.Location.str.contains('Minneapolis'), 'climate'] = 'Cold Climate'
df.loc[df.Location.str.contains('Chicago'), 'climate'] = 'Swing Climate'
df.loc[df.Location.str.contains('Miami'), 'climate'] = 'Hot Climate'
df.loc[df.Location.str.contains('LosAngeles'), 'climate'] = 'Other Climate'


#####
# Create pivot table of NPV of System Costs
cost = df.pivot_table(index= 'climate',
                        columns= 'Building Type',
                        values = 'Value',
                        ).reindex(index = ['Cold Climate','Swing Climate', 'Hot Climate', 'Other Climate'])

cold = list(cost.loc['Cold Climate',:].dropna().values)
swing = list(cost.loc['Swing Climate',:].dropna().values)
hot = list(cost.loc['Hot Climate',:].dropna().values)
other = list(cost.loc['Other Climate',:].dropna().values)

ticks = ['Cold Climate',
         'Swing Climate', 
         'Hot Climate', 
         'Other Climate']

def set_box_color(bp, color_selection):
    plt.setp(bp['boxes'], color=color_selection, alpha=0.8)
    plt.setp(bp['whiskers'], color=color_selection)
    plt.setp(bp['caps'], color=color_selection)
    plt.setp(bp['medians'], color=color_selection)
    
plt.figure(figsize=(9,6))

flierprops = dict(marker='o',
                  markerfacecolor = 'black',
                  markersize=8, 
                  linestyle='none',
                  markeredgecolor='black'
                  )

boxplot = plt.boxplot([cold, swing, hot, other],
                      patch_artist=True,
                      whis=(0,100),
                      labels=ticks,
#                      flierprops=flierprops,
                      )
color_palette = {'blue':['#0B5E90', '#0079C2', '#00A4E4', '#5DD2FF'],
                 'yellow': ['#A16911', '#F7A11A', '#FFC423', '#FFD200'],
                 'green': ['#3D6321', '#5D9732', '#8CC63F', '#C1EE86'],
                 'orange': ['#6F2D01', '#933C06', '#D9531E', '#FE6523'],
                 'gray': ['#4B545A', '#5E6A71', '#D1D5D8', '#DEE2E5'],
                 'black': ['#000000', '#212121', '#282D30', '#3A4246']}
box_color_selection = {'cold': color_palette['green'][1],
                       'swing': color_palette['blue'][1],
                       'hot': color_palette['orange'][1],
                       'other': color_palette['gray'][1]}
colors = (box_color_selection['cold'],
          box_color_selection['swing'],
          box_color_selection['hot'],
          box_color_selection['other']
          )

plt.rc('xtick',labelsize=12)
plt.rc('ytick',labelsize=12)
plt.grid( axis='y', linewidth=0.75, color ='#D9D9D9', zorder=0)
#plt.yticks(np.arange(-900, 900, 100))

# CUSTOM BOXPLOT OPTIONS
for i in range(len(colors)):
    plt.setp(boxplot['boxes'][i], color=colors[i], alpha=0.75)
    plt.setp(boxplot['whiskers'][2*i:2*i+2], color=colors[i])
    plt.setp(boxplot['caps'][2*i:2*i+2], color=colors[i])
    plt.setp(boxplot['medians'][i], color=colors[i])

for box in boxplot['boxes']:
    box.set(linewidth=3)

for median in boxplot['medians']:
    median.set(color='black', linewidth=2, zorder=10)

for flier in boxplot['fliers']:
    flier.set(marker='o', color='orange', alpha=1)

for pos in ['right','left']:
    plt.gca().spines[pos].set_visible(False)

plt.ylabel("Net Costs (thousand $)", fontweight='bold', fontsize=14)#, fontsize=14)

plt.savefig(os.path.join(dir, "results", "figures", "net_saving.png"), dpi=600, bbox_inches='tight')

#####
# Create pivot table of NPV of Fuel Costs
cost = df.pivot_table(index= 'climate',
                        columns= 'Building Type',
                        values = 'Fuel Cost Savings',
                        ).reindex(index = ['Cold Climate','Swing Climate', 'Hot Climate', 'Other Climate'])

cold = list(cost.loc['Cold Climate',:].dropna().values)
swing = list(cost.loc['Swing Climate',:].dropna().values)
hot = list(cost.loc['Hot Climate',:].dropna().values)
other = list(cost.loc['Other Climate',:].dropna().values)

ticks = ['Cold Climate',
         'Swing Climate', 
         'Hot Climate', 
         'Other Climate']
    
plt.figure(figsize=(9,6))

flierprops = dict(marker='o',
                  markerfacecolor = 'black',
                  markersize=8, 
                  linestyle='none',
                  markeredgecolor='black'
                  )

boxplot = plt.boxplot([cold, swing, hot, other],
                      patch_artist=True,
                      whis=(0,100),
                      labels=ticks,
#                      flierprops=flierprops,
                      )
color_palette = {'blue':['#0B5E90', '#0079C2', '#00A4E4', '#5DD2FF'],
                 'yellow': ['#A16911', '#F7A11A', '#FFC423', '#FFD200'],
                 'green': ['#3D6321', '#5D9732', '#8CC63F', '#C1EE86'],
                 'orange': ['#6F2D01', '#933C06', '#D9531E', '#FE6523'],
                 'gray': ['#4B545A', '#5E6A71', '#D1D5D8', '#DEE2E5'],
                 'black': ['#000000', '#212121', '#282D30', '#3A4246']}
box_color_selection = {'cold': color_palette['green'][1],
                       'swing': color_palette['blue'][1],
                       'hot': color_palette['orange'][1],
                       'other': color_palette['gray'][1]}
colors = (box_color_selection['cold'],
          box_color_selection['swing'],
          box_color_selection['hot'],
          box_color_selection['other']
          )

plt.rc('xtick',labelsize=12)
plt.rc('ytick',labelsize=12)
plt.grid( axis='y', linewidth=0.75, color ='#D9D9D9', zorder=0)
plt.ylabel('Fuel Cost Savings (thousand $)', size = 20, weight='bold')
#plt.yticks(np.arange(-900, 900, 100))

# CUSTOM BOXPLOT OPTIONS
for i in range(len(colors)):
    plt.setp(boxplot['boxes'][i], color=colors[i], alpha=0.75)
    plt.setp(boxplot['whiskers'][2*i:2*i+2], color=colors[i])
    plt.setp(boxplot['caps'][2*i:2*i+2], color=colors[i])
    plt.setp(boxplot['medians'][i], color=colors[i])

for box in boxplot['boxes']:
    box.set(linewidth=3)

for median in boxplot['medians']:
    median.set(color='black', linewidth=2, zorder=10)

for flier in boxplot['fliers']:
    flier.set(marker='o', color='orange', alpha=1)

for pos in ['right','left']:
    plt.gca().spines[pos].set_visible(False)

plt.ylabel("Fuel Cost Savings (thousand $)", fontweight='bold', fontsize=14)#, fontsize=14)

plt.savefig(os.path.join(dir, "results", "figures", "fuel_npv.png"), dpi=600, bbox_inches='tight')

# Create pivot table of NPV of Electricity Bill Increase
cost = df.pivot_table(index= 'climate',
                        columns= 'Building Type',
                        values = 'NPV-Elec Bill',
                        ).reindex(index = ['Cold Climate','Swing Climate', 'Hot Climate', 'Other Climate'])

cold = list(cost.loc['Cold Climate',:].dropna().values)
swing = list(cost.loc['Swing Climate',:].dropna().values)
hot = list(cost.loc['Hot Climate',:].dropna().values)
other = list(cost.loc['Other Climate',:].dropna().values)

ticks = ['Cold Climate',
         'Swing Climate', 
         'Hot Climate', 
         'Other Climate']
    
plt.figure(figsize=(9,6))

flierprops = dict(marker='o',
                  markerfacecolor = 'black',
                  markersize=8, 
                  linestyle='none',
                  markeredgecolor='black'
                  )

boxplot = plt.boxplot([cold, swing, hot, other],
                      patch_artist=True,
                      whis=(0,100),
                      labels=ticks,
#                      flierprops=flierprops,
                      )
color_palette = {'blue':['#0B5E90', '#0079C2', '#00A4E4', '#5DD2FF'],
                 'yellow': ['#A16911', '#F7A11A', '#FFC423', '#FFD200'],
                 'green': ['#3D6321', '#5D9732', '#8CC63F', '#C1EE86'],
                 'orange': ['#6F2D01', '#933C06', '#D9531E', '#FE6523'],
                 'gray': ['#4B545A', '#5E6A71', '#D1D5D8', '#DEE2E5'],
                 'black': ['#000000', '#212121', '#282D30', '#3A4246']}
box_color_selection = {'cold': color_palette['green'][1],
                       'swing': color_palette['blue'][1],
                       'hot': color_palette['orange'][1],
                       'other': color_palette['gray'][1]}
colors = (box_color_selection['cold'],
          box_color_selection['swing'],
          box_color_selection['hot'],
          box_color_selection['other']
          )

plt.rc('xtick',labelsize=12)
plt.rc('ytick',labelsize=12)
plt.grid( axis='y', linewidth=0.75, color ='#D9D9D9', zorder=0)
#plt.yticks(np.arange(-900, 900, 100))

# CUSTOM BOXPLOT OPTIONS
for i in range(len(colors)):
    plt.setp(boxplot['boxes'][i], color=colors[i], alpha=0.75)
    plt.setp(boxplot['whiskers'][2*i:2*i+2], color=colors[i])
    plt.setp(boxplot['caps'][2*i:2*i+2], color=colors[i])
    plt.setp(boxplot['medians'][i], color=colors[i])

for box in boxplot['boxes']:
    box.set(linewidth=3)

for median in boxplot['medians']:
    median.set(color='black', linewidth=2, zorder=10)

for flier in boxplot['fliers']:
    flier.set(marker='o', color='orange', alpha=1)

for pos in ['right','left']:
    plt.gca().spines[pos].set_visible(False)

plt.ylabel("Electricity Bill Increase (thousand $)", fontweight='bold', fontsize=14)#, fontsize=14)

plt.savefig(os.path.join(dir, "results", "figures", "elec_npv.png"), dpi=600, bbox_inches='tight')

# Create pivot table of NPV of Total Bill Increase
cost = df.pivot_table(index= 'climate',
                        columns= 'Building Type',
                        values = 'Bill Increase',
                        ).reindex(index = ['Cold Climate','Swing Climate', 'Hot Climate', 'Other Climate'])

cold = list(cost.loc['Cold Climate',:].dropna().values)
swing = list(cost.loc['Swing Climate',:].dropna().values)
hot = list(cost.loc['Hot Climate',:].dropna().values)
other = list(cost.loc['Other Climate',:].dropna().values)

ticks = ['Cold Climate',
         'Swing Climate', 
         'Hot Climate', 
         'Other Climate']
    
plt.figure(figsize=(9,6))

flierprops = dict(marker='o',
                  markerfacecolor = 'black',
                  markersize=8, 
                  linestyle='none',
                  markeredgecolor='black'
                  )

boxplot = plt.boxplot([cold, swing, hot, other],
                      patch_artist=True,
                      whis=(0,100),
                      labels=ticks,
#                      flierprops=flierprops,
                      )
color_palette = {'blue':['#0B5E90', '#0079C2', '#00A4E4', '#5DD2FF'],
                 'yellow': ['#A16911', '#F7A11A', '#FFC423', '#FFD200'],
                 'green': ['#3D6321', '#5D9732', '#8CC63F', '#C1EE86'],
                 'orange': ['#6F2D01', '#933C06', '#D9531E', '#FE6523'],
                 'gray': ['#4B545A', '#5E6A71', '#D1D5D8', '#DEE2E5'],
                 'black': ['#000000', '#212121', '#282D30', '#3A4246']}
box_color_selection = {'cold': color_palette['green'][1],
                       'swing': color_palette['blue'][1],
                       'hot': color_palette['orange'][1],
                       'other': color_palette['gray'][1]}
colors = (box_color_selection['cold'],
          box_color_selection['swing'],
          box_color_selection['hot'],
          box_color_selection['other']
          )

plt.rc('xtick',labelsize=12)
plt.rc('ytick',labelsize=12)
plt.grid( axis='y', linewidth=0.75, color ='#D9D9D9', zorder=0)
#plt.yticks(np.arange(-900, 900, 100))

# CUSTOM BOXPLOT OPTIONS
for i in range(len(colors)):
    plt.setp(boxplot['boxes'][i], color=colors[i], alpha=0.75)
    plt.setp(boxplot['whiskers'][2*i:2*i+2], color=colors[i])
    plt.setp(boxplot['caps'][2*i:2*i+2], color=colors[i])
    plt.setp(boxplot['medians'][i], color=colors[i])

for box in boxplot['boxes']:
    box.set(linewidth=3)

for median in boxplot['medians']:
    median.set(color='black', linewidth=2, zorder=10)

for flier in boxplot['fliers']:
    flier.set(marker='o', color='orange', alpha=1)

for pos in ['right','left']:
    plt.gca().spines[pos].set_visible(False)

plt.ylabel("Total Bill Increase (thousand $)", fontweight='bold', fontsize=14)#, fontsize=14)

plt.savefig(os.path.join(dir, "results", "figures", "bill_npv.png"), dpi=600, bbox_inches='tight')

#####
# Create pivot table of LCCC
cost = df.pivot_table(index= 'climate',
                        columns= 'Building Type',
                        values = 'LCCC',
                        ).reindex(index = ['Cold Climate','Swing Climate', 'Hot Climate', 'Other Climate'])

cold = list(cost.loc['Cold Climate',:].dropna().values)
swing = list(cost.loc['Swing Climate',:].dropna().values)
hot = list(cost.loc['Hot Climate',:].dropna().values)
other = list(cost.loc['Other Climate',:].dropna().values)

ticks = ['Cold Climate',
         'Swing Climate', 
         'Hot Climate', 
         'Other Climate']
    
plt.figure(figsize=(9,6))

flierprops = dict(marker='o',
                  markerfacecolor = 'black',
                  markersize=8, 
                  linestyle='none',
                  markeredgecolor='black'
                  )

boxplot = plt.boxplot([cold, swing, hot, other],
                      patch_artist=True,
                      whis=(0,100),
                      labels=ticks,
#                      flierprops=flierprops,
                      )
color_palette = {'blue':['#0B5E90', '#0079C2', '#00A4E4', '#5DD2FF'],
                 'yellow': ['#A16911', '#F7A11A', '#FFC423', '#FFD200'],
                 'green': ['#3D6321', '#5D9732', '#8CC63F', '#C1EE86'],
                 'orange': ['#6F2D01', '#933C06', '#D9531E', '#FE6523'],
                 'gray': ['#4B545A', '#5E6A71', '#D1D5D8', '#DEE2E5'],
                 'black': ['#000000', '#212121', '#282D30', '#3A4246']}
box_color_selection = {'cold': color_palette['green'][1],
                       'swing': color_palette['blue'][1],
                       'hot': color_palette['orange'][1],
                       'other': color_palette['gray'][1]}
colors = (box_color_selection['cold'],
          box_color_selection['swing'],
          box_color_selection['hot'],
          box_color_selection['other']
          )

plt.rc('xtick',labelsize=12)
plt.rc('ytick',labelsize=12)
plt.grid( axis='y', linewidth=0.75, color ='#D9D9D9', zorder=0)
plt.ylabel('Lifecycle Capital Costs (thousand $)', size = 20, weight='bold')
#plt.yticks(np.arange(-900, 900, 100))

# CUSTOM BOXPLOT OPTIONS
for i in range(len(colors)):
    plt.setp(boxplot['boxes'][i], color=colors[i], alpha=0.75)
    plt.setp(boxplot['whiskers'][2*i:2*i+2], color=colors[i])
    plt.setp(boxplot['caps'][2*i:2*i+2], color=colors[i])
    plt.setp(boxplot['medians'][i], color=colors[i])

for box in boxplot['boxes']:
    box.set(linewidth=3)

for median in boxplot['medians']:
    median.set(color='black', linewidth=2, zorder=10)

for flier in boxplot['fliers']:
    flier.set(marker='o', color='orange', alpha=1)

for pos in ['right','left']:
    plt.gca().spines[pos].set_visible(False)

plt.ylabel("Lifecycle Capital Costs (thousand $)", fontweight='bold', fontsize=14)#, fontsize=14)

plt.savefig(os.path.join(dir, "results", "figures", "lccc.png"), dpi=600, bbox_inches='tight')


#####
# Create pivot table of Cost/ton
cost = df.pivot_table(index= 'climate',
                        columns= 'Building Type',
                        values = 'Cost per ton',
                        ).reindex(index = ['Cold Climate','Swing Climate', 'Hot Climate', 'Other Climate'])

cold = list(cost.loc['Cold Climate',:].dropna().values)
swing = list(cost.loc['Swing Climate',:].dropna().values)
hot = list(cost.loc['Hot Climate',:].dropna().values)
other = list(cost.loc['Other Climate',:].dropna().values)

ticks = ['Cold Climate',
         'Swing Climate', 
         'Hot Climate', 
         'Other Climate']
    
plt.figure(figsize=(9,6))

flierprops = dict(marker='o',
                  markerfacecolor = 'black',
                  markersize=8, 
                  linestyle='none',
                  markeredgecolor='black'
                  )

boxplot = plt.boxplot([cold, swing, hot, other],
                      patch_artist=True,
                      whis=(0,100),
                      labels=ticks,
#                      flierprops=flierprops,
                      )
color_palette = {'blue':['#0B5E90', '#0079C2', '#00A4E4', '#5DD2FF'],
                 'yellow': ['#A16911', '#F7A11A', '#FFC423', '#FFD200'],
                 'green': ['#3D6321', '#5D9732', '#8CC63F', '#C1EE86'],
                 'orange': ['#6F2D01', '#933C06', '#D9531E', '#FE6523'],
                 'gray': ['#4B545A', '#5E6A71', '#D1D5D8', '#DEE2E5'],
                 'black': ['#000000', '#212121', '#282D30', '#3A4246']}
box_color_selection = {'cold': color_palette['green'][1],
                       'swing': color_palette['blue'][1],
                       'hot': color_palette['orange'][1],
                       'other': color_palette['gray'][1]}
colors = (box_color_selection['cold'],
          box_color_selection['swing'],
          box_color_selection['hot'],
          box_color_selection['other']
          )

plt.rc('xtick',labelsize=12)
plt.rc('ytick',labelsize=12)
plt.grid( axis='y', linewidth=0.75, color ='#D9D9D9', zorder=0)
plt.ylabel('Cost per ton ($)', size = 20, weight='bold')
#plt.yticks(np.arange(-900, 900, 100))

# CUSTOM BOXPLOT OPTIONS
for i in range(len(colors)):
    plt.setp(boxplot['boxes'][i], color=colors[i], alpha=0.75)
    plt.setp(boxplot['whiskers'][2*i:2*i+2], color=colors[i])
    plt.setp(boxplot['caps'][2*i:2*i+2], color=colors[i])
    plt.setp(boxplot['medians'][i], color=colors[i])

for box in boxplot['boxes']:
    box.set(linewidth=3)

for median in boxplot['medians']:
    median.set(color='black', linewidth=2, zorder=10)

for flier in boxplot['fliers']:
    flier.set(marker='o', color='orange', alpha=1)

for pos in ['right','left']:
    plt.gca().spines[pos].set_visible(False)

plt.ylabel("Cost per ton ($)", fontweight='bold', fontsize=14)#, fontsize=14)

plt.savefig(os.path.join(dir, "results", "figures", "cost_per_ton.png"), dpi=600, bbox_inches='tight')


#####
# Create pivot table of Avoided Health Damages
cost = df.pivot_table(index= 'climate',
                        columns= 'Building Type',
                        values = 'Avoided Health Damages [T$]',
                        ).reindex(index = ['Cold Climate','Swing Climate', 'Hot Climate', 'Other Climate'])

cold = list(cost.loc['Cold Climate',:].dropna().values)
swing = list(cost.loc['Swing Climate',:].dropna().values)
hot = list(cost.loc['Hot Climate',:].dropna().values)
other = list(cost.loc['Other Climate',:].dropna().values)

ticks = ['Cold Climate',
         'Swing Climate', 
         'Hot Climate', 
         'Other Climate']
    
plt.figure(figsize=(9,6))

flierprops = dict(marker='o',
                  markerfacecolor = 'black',
                  markersize=8, 
                  linestyle='none',
                  markeredgecolor='black'
                  )

boxplot = plt.boxplot([cold, swing, hot, other],
                      patch_artist=True,
                      whis=(0,100),
                      labels=ticks,
#                      flierprops=flierprops,
                      )
color_palette = {'blue':['#0B5E90', '#0079C2', '#00A4E4', '#5DD2FF'],
                 'yellow': ['#A16911', '#F7A11A', '#FFC423', '#FFD200'],
                 'green': ['#3D6321', '#5D9732', '#8CC63F', '#C1EE86'],
                 'orange': ['#6F2D01', '#933C06', '#D9531E', '#FE6523'],
                 'gray': ['#4B545A', '#5E6A71', '#D1D5D8', '#DEE2E5'],
                 'black': ['#000000', '#212121', '#282D30', '#3A4246']}
box_color_selection = {'cold': color_palette['green'][1],
                       'swing': color_palette['blue'][1],
                       'hot': color_palette['orange'][1],
                       'other': color_palette['gray'][1]}
colors = (box_color_selection['cold'],
          box_color_selection['swing'],
          box_color_selection['hot'],
          box_color_selection['other']
          )

plt.rc('xtick',labelsize=12)
plt.rc('ytick',labelsize=12)
plt.grid( axis='y', linewidth=0.75, color ='#D9D9D9', zorder=0)
plt.ylabel('Cost per ton ($)', size = 20, weight='bold')
#plt.yticks(np.arange(-900, 900, 100))

# CUSTOM BOXPLOT OPTIONS
for i in range(len(colors)):
    plt.setp(boxplot['boxes'][i], color=colors[i], alpha=0.75)
    plt.setp(boxplot['whiskers'][2*i:2*i+2], color=colors[i])
    plt.setp(boxplot['caps'][2*i:2*i+2], color=colors[i])
    plt.setp(boxplot['medians'][i], color=colors[i])

for box in boxplot['boxes']:
    box.set(linewidth=3)

for median in boxplot['medians']:
    median.set(color='black', linewidth=2, zorder=10)

for flier in boxplot['fliers']:
    flier.set(marker='o', color='orange', alpha=1)

for pos in ['right','left']:
    plt.gca().spines[pos].set_visible(False)

plt.ylabel("Avoided Health Damages (thousand $)", fontweight='bold', fontsize=14)#, fontsize=14)

plt.savefig(os.path.join(dir, "results", "figures", "avoided_health_damages.png"), dpi=600, bbox_inches='tight')


#####
# Create pivot table of Co2 emission savings
cost = df.pivot_table(index= 'climate',
                        columns= 'Building Type',
                        values = 'CO2 Emission Saving [kTonne]',
                        ).reindex(index = ['Cold Climate','Swing Climate', 'Hot Climate', 'Other Climate'])

cold = list(cost.loc['Cold Climate',:].dropna().values)
swing = list(cost.loc['Swing Climate',:].dropna().values)
hot = list(cost.loc['Hot Climate',:].dropna().values)
other = list(cost.loc['Other Climate',:].dropna().values)

ticks = ['Cold Climate',
         'Swing Climate', 
         'Hot Climate', 
         'Other Climate']
    
plt.figure(figsize=(9,6))

flierprops = dict(marker='o',
                  markerfacecolor = 'black',
                  markersize=8, 
                  linestyle='none',
                  markeredgecolor='black'
                  )

boxplot = plt.boxplot([cold, swing, hot, other],
                      patch_artist=True,
                      whis=(0,100),
                      labels=ticks,
#                      flierprops=flierprops,
                      )
color_palette = {'blue':['#0B5E90', '#0079C2', '#00A4E4', '#5DD2FF'],
                 'yellow': ['#A16911', '#F7A11A', '#FFC423', '#FFD200'],
                 'green': ['#3D6321', '#5D9732', '#8CC63F', '#C1EE86'],
                 'orange': ['#6F2D01', '#933C06', '#D9531E', '#FE6523'],
                 'gray': ['#4B545A', '#5E6A71', '#D1D5D8', '#DEE2E5'],
                 'black': ['#000000', '#212121', '#282D30', '#3A4246']}
box_color_selection = {'cold': color_palette['green'][1],
                       'swing': color_palette['blue'][1],
                       'hot': color_palette['orange'][1],
                       'other': color_palette['gray'][1]}
colors = (box_color_selection['cold'],
          box_color_selection['swing'],
          box_color_selection['hot'],
          box_color_selection['other']
          )

plt.rc('xtick',labelsize=12)
plt.rc('ytick',labelsize=12)
plt.grid( axis='y', linewidth=0.75, color ='#D9D9D9', zorder=0)
plt.ylabel('Cost per ton ($)', size = 20, weight='bold')
#plt.yticks(np.arange(-900, 900, 100))

# CUSTOM BOXPLOT OPTIONS
for i in range(len(colors)):
    plt.setp(boxplot['boxes'][i], color=colors[i], alpha=0.75)
    plt.setp(boxplot['whiskers'][2*i:2*i+2], color=colors[i])
    plt.setp(boxplot['caps'][2*i:2*i+2], color=colors[i])
    plt.setp(boxplot['medians'][i], color=colors[i])

for box in boxplot['boxes']:
    box.set(linewidth=3)

for median in boxplot['medians']:
    median.set(color='black', linewidth=2, zorder=10)

for flier in boxplot['fliers']:
    flier.set(marker='o', color='orange', alpha=1)

for pos in ['right','left']:
    plt.gca().spines[pos].set_visible(False)

plt.ylabel("CO2 Emission Saving (thousand tons)", fontweight='bold', fontsize=14)#, fontsize=14)

plt.savefig(os.path.join(dir, "results", "figures", "co2_savings.png"), dpi=600, bbox_inches='tight')



#####
# Create pivot table of ASHP Sizing (ASHP SH)
cost = df.pivot_table(index= 'climate',
                        columns= 'Building Type',
                        values = 'ASHP-SH Size [ton]',
                        ).reindex(index = ['Cold Climate','Swing Climate', 'Hot Climate', 'Other Climate'])

cold = list(cost.loc['Cold Climate',:].dropna().values)
swing = list(cost.loc['Swing Climate',:].dropna().values)
hot = list(cost.loc['Hot Climate',:].dropna().values)
other = list(cost.loc['Other Climate',:].dropna().values)

ticks = ['Cold Climate',
         'Swing Climate', 
         'Hot Climate', 
         'Other Climate']
    
plt.figure(figsize=(9,6))

flierprops = dict(marker='o',
                  markerfacecolor = 'black',
                  markersize=8, 
                  linestyle='none',
                  markeredgecolor='black'
                  )

boxplot = plt.boxplot([cold, swing, hot, other],
                      patch_artist=True,
                      whis=(0,100),
                      labels=ticks,
#                      flierprops=flierprops,
                      )
color_palette = {'blue':['#0B5E90', '#0079C2', '#00A4E4', '#5DD2FF'],
                 'yellow': ['#A16911', '#F7A11A', '#FFC423', '#FFD200'],
                 'green': ['#3D6321', '#5D9732', '#8CC63F', '#C1EE86'],
                 'orange': ['#6F2D01', '#933C06', '#D9531E', '#FE6523'],
                 'gray': ['#4B545A', '#5E6A71', '#D1D5D8', '#DEE2E5'],
                 'black': ['#000000', '#212121', '#282D30', '#3A4246']}
box_color_selection = {'cold': color_palette['green'][1],
                       'swing': color_palette['blue'][1],
                       'hot': color_palette['orange'][1],
                       'other': color_palette['gray'][1]}
colors = (box_color_selection['cold'],
          box_color_selection['swing'],
          box_color_selection['hot'],
          box_color_selection['other']
          )

plt.rc('xtick',labelsize=12)
plt.rc('ytick',labelsize=12)
plt.grid( axis='y', linewidth=0.75, color ='#D9D9D9', zorder=0)
plt.ylabel('Cost per ton ($)', size = 20, weight='bold')
#plt.yticks(np.arange(-900, 900, 100))

# CUSTOM BOXPLOT OPTIONS
for i in range(len(colors)):
    plt.setp(boxplot['boxes'][i], color=colors[i], alpha=0.75)
    plt.setp(boxplot['whiskers'][2*i:2*i+2], color=colors[i])
    plt.setp(boxplot['caps'][2*i:2*i+2], color=colors[i])
    plt.setp(boxplot['medians'][i], color=colors[i])

for box in boxplot['boxes']:
    box.set(linewidth=3)

for median in boxplot['medians']:
    median.set(color='black', linewidth=2, zorder=10)

for flier in boxplot['fliers']:
    flier.set(marker='o', color='orange', alpha=1)

for pos in ['right','left']:
    plt.gca().spines[pos].set_visible(False)

plt.ylabel("ASHP-SH Size (ton)", fontweight='bold', fontsize=14)#, fontsize=14)

plt.savefig(os.path.join(dir, "results", "figures", "ashp_sh_size.png"), dpi=600, bbox_inches='tight')



# Create pivot table of ASHP Sizing (ASHP WH)
cost = df.pivot_table(index= 'climate',
                        columns= 'Building Type',
                        values = 'ASHP-WH Size [ton]',
                        ).reindex(index = ['Cold Climate','Swing Climate', 'Hot Climate', 'Other Climate'])

cold = list(cost.loc['Cold Climate',:].dropna().values)
swing = list(cost.loc['Swing Climate',:].dropna().values)
hot = list(cost.loc['Hot Climate',:].dropna().values)
other = list(cost.loc['Other Climate',:].dropna().values)

ticks = ['Cold Climate',
         'Swing Climate', 
         'Hot Climate', 
         'Other Climate']
    
plt.figure(figsize=(9,6))

flierprops = dict(marker='o',
                  markerfacecolor = 'black',
                  markersize=8, 
                  linestyle='none',
                  markeredgecolor='black'
                  )

boxplot = plt.boxplot([cold, swing, hot, other],
                      patch_artist=True,
                      whis=(0,100),
                      labels=ticks,
#                      flierprops=flierprops,
                      )
color_palette = {'blue':['#0B5E90', '#0079C2', '#00A4E4', '#5DD2FF'],
                 'yellow': ['#A16911', '#F7A11A', '#FFC423', '#FFD200'],
                 'green': ['#3D6321', '#5D9732', '#8CC63F', '#C1EE86'],
                 'orange': ['#6F2D01', '#933C06', '#D9531E', '#FE6523'],
                 'gray': ['#4B545A', '#5E6A71', '#D1D5D8', '#DEE2E5'],
                 'black': ['#000000', '#212121', '#282D30', '#3A4246']}
box_color_selection = {'cold': color_palette['green'][1],
                       'swing': color_palette['blue'][1],
                       'hot': color_palette['orange'][1],
                       'other': color_palette['gray'][1]}
colors = (box_color_selection['cold'],
          box_color_selection['swing'],
          box_color_selection['hot'],
          box_color_selection['other']
          )

plt.rc('xtick',labelsize=12)
plt.rc('ytick',labelsize=12)
plt.grid( axis='y', linewidth=0.75, color ='#D9D9D9', zorder=0)
plt.ylabel('Cost per ton ($)', size = 20, weight='bold')
#plt.yticks(np.arange(-900, 900, 100))

# CUSTOM BOXPLOT OPTIONS
for i in range(len(colors)):
    plt.setp(boxplot['boxes'][i], color=colors[i], alpha=0.75)
    plt.setp(boxplot['whiskers'][2*i:2*i+2], color=colors[i])
    plt.setp(boxplot['caps'][2*i:2*i+2], color=colors[i])
    plt.setp(boxplot['medians'][i], color=colors[i])

for box in boxplot['boxes']:
    box.set(linewidth=3)

for median in boxplot['medians']:
    median.set(color='black', linewidth=2, zorder=10)

for flier in boxplot['fliers']:
    flier.set(marker='o', color='orange', alpha=1)

for pos in ['right','left']:
    plt.gca().spines[pos].set_visible(False)

plt.ylabel("ASHP-WH Size (ton)", fontweight='bold', fontsize=14)#, fontsize=14)

plt.savefig(os.path.join(dir, "results", "figures", "ashp_wh_size.png"), dpi=600, bbox_inches='tight')