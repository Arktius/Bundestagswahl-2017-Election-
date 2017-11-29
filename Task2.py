# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 20:23:52 2017

@author: Denis Baskan

Task2:
Displays a bar chart of the Zweitstimmen result of the elections. Uses pyplot to draw the diagram.

The diagram looks similar to https://www.bundeswahlleiter.de/bundestagswahlen/2017/ergebnisse.html.
Uses color codes for the parties, and combines every party below 5% into Sonstige.
Displays the numeric values at the top of the bar.

"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

#%pylab 

#set console working directory manually
#get path of csv file
path = os.path.realpath('ergebnisse.csv')
#path = 'D:\Baskan\ergebnisse.csv'

#importing the dataset into data frame
ds = pd.read_csv(path, delimiter=';')

#drop unnecessary columns
ds = ds[['gruppe','zweitstimmen']]

#drop data where gruppe is 'Wahlberechtigte', 'Wähler' or 'Ungültige'
ds = ds[~ds['gruppe'].isin(['Wahlberechtigte','Wähler','Ungültige'])]
ds = ds.reset_index(drop=True)

#replace '-' by 0 for 'zweitstimmen'
ds['zweitstimmen'] = ds['zweitstimmen'].replace(to_replace ='-', value=0)

#convert 'zweitstimmen' to integer
ds.loc[:,('zweitstimmen')] = ds.loc[:,('zweitstimmen')].astype(int)

#erase the dot at the end (e.g. 'DIE LINKE.')
#ds['gruppe'] = ds['gruppe'].map(lambda x: x.rstrip('.')) 
ds.loc[:,('gruppe')] = ds.loc[:,('gruppe')].map(lambda x: x.rstrip('.')) 

#seperate valid_votes from data frame
valid_votes = ds[ds['gruppe'] == 'Gültige']
ds = ds[ds['gruppe'] != 'Gültige']
ds = ds.reset_index(drop = True)

#sum up 'zweitsimmen' by party
votes2 = ds.groupby(['gruppe'])['zweitstimmen'].sum()
votes2 = votes2.reset_index()
#drop data with 0 zweitstimmen
votes2 = votes2[votes2['zweitstimmen']> 0]

#calculate percantages for each party
result = pd.DataFrame({'Party' : [] , 'Percentage' : []})
result['Party'] = votes2['gruppe']
result['Percentage'] = 100*(votes2['zweitstimmen'] / valid_votes['zweitstimmen'].sum())

#sort parties descending and show it in terminal
result = result.sort_values(by = 'Percentage', ascending = False )
result = result.reset_index(drop = True)

#CSV Output
print('Task 1:')
print(result.to_csv(sep = ';',index = False))

#%% Task2

#replace GRÜNE/B 90 by 'GRÜNE'
result['Party'] = result['Party'].replace(to_replace = 'GRÜNE/B 90', value = 'GRÜNE')
#replace ÖDP / Familie by 'ÖDP'
result['Party'] = result['Party'].replace(to_replace = 'ÖDP / Familie ', value = 'ÖDP')

#seperate parties with zweitstimmen < 5%
votes2 = result.groupby(['Party'])['Percentage'].sum()
votes2 = votes2.reset_index()
others = votes2[votes2['Percentage']  < 5]
votes2 = votes2[votes2['Percentage']  >= 5]

#add 'others'
votes2.loc[len(votes2)] = ['others' , others['Percentage'].sum()]

#sort parties by zweitstimmen
votes2 = votes2.sort_values(by = 'Percentage', ascending = False)
votes2 = votes2.reset_index(drop = True)


#number of parties (+1 for others)
n = votes2.count()[0]

#set plot size
plotwidth = 10
plotheight = 5

#indentations of bars and texts
ind = np.linspace(1,plotwidth/1.5,n)
#width of bars
width = 0.5 

#map colors (RGB)
#CDU - (68,68,138)
#SPD (204,0,51)
#AfD (54,202,197)
#FDP (255,204,51)
#DIE LINKE (143,87,199)
#GRÜNE (50,164,96)
#CSU (0,137,196)
#others (211,211,211)

#RGB-colors of parties [0,1]
colors = [(68,68,138),(204,0,51),(54,202,197),(255,204,51),(143,87,199),(50,164,96),(0,137,196),(211,211,211)]
colors = np.divide(colors,255)     

#plot bars
p1 = plt.bar(ind, votes2['Percentage'], width, color= colors)#[1,0,0])

#set figure width and height 
#plt.rcParams["figure.figsize"] = [plotwidth,plotheight] #fig_size


#write labels, title 
plt.xlabel('Parteien')
plt.ylabel('Zweitstimmen in %')
plt.title('Bundestagswahlen 2017')
plt.xticks(0.2+ind, votes2['Party'])
plt.yticks(np.arange(0, max(result['Percentage'])+5, 5))

#write percentages over bars
for i in range(0,ind.size):
    plt.text(ind[i],votes2['Percentage'][i]+0.5,round(votes2['Percentage'][i], ndigits = 1))


#save plot
plt.savefig('Diagram.png',dpi = 900) #dpi is the resolution

print('Task 2:')
#show chart
plt.show()


