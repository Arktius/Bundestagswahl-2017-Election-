# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 20:23:52 2017

@author: Denis Baskan 

Task:
Compute the percentage of Zweitstimmen for each political party in the 2017 Bundestagswahlen, 
using ergebnisse.csv as your data source.
Upload a Python script to this assignment that produces the results as a CSV output to the terminal, 
in the format

Party;Percentage

"""

import pandas as pd
import os

#set console working directory manually
#get path of csv file
path = os.path.realpath('ergebnisse.csv')

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
print(result.to_csv(sep = ';',index = False))
#save as csv file
print(result.to_csv(path_or_buf = 'result.csv',sep = ';',index = False))
