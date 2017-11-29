# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 10:13:09 2017

@author: Denis Baskan MNr. : 878 571

Task 3

For this and the next exercise, familiarize yourself with the procedure for seat distribution in the Bundestag.

* Method of Sainte-Laguë/Schepers
* Computation of Mindestsitzzahl

For this assignment, compute the Mindestsitzzahl for each party and each state.

Implement the method of Saint-Lesque/Schepers in a reusable manner
For each constituency, compute the winning party of the direct seat (Direktmandat). For each state, compute the number of direct seats per party
Compute a distribution of 598 seats to the states, according to the population count in population.csv (source: bundeswahlleiter.de)
For each state, compute the assignment of seats to the parties according to the share of Zweitstimmen.
Print out a list of states (by name) and parties with number of direct seats and list seats, as well as the number of seats by  which the direct seats are larger than the list seats (Überhangmandate) (0 if the number is not larger). Produce a CSV output of the form
state;party;direct_seats;list_seats;ueberhang

"""
print('\nAssignment 3 - Denis Baskan - MNr.: 878 571\n')

import pandas as pd
import os
import numpy as np

#set console working directory manually
#get path of csv file
path = os.path.realpath('ergebnisse.csv')

#importing the dataset into data frame
ds = pd.read_csv(path, delimiter=';')

#drop data where gruppe is 'Wahlberechtigte', 'Wähler' or 'Ungültige'
ds = ds[~ds['gruppe'].isin(['Wahlberechtigte','Wähler','Ungültige'])].reset_index(drop = True)

#replace '-' by 0 and convert into integer
ds['zweitstimmen'] = ds['zweitstimmen'].replace(to_replace ='-', value=0).astype(int)
ds['erststimmen'] = ds['erststimmen'].replace(to_replace ='-', value=0).astype(int)

#erase the dot at the end (e.g. 'DIE LINKE.')
ds.loc[:,('gruppe')] = ds.loc[:,('gruppe')].map(lambda x: x.rstrip('.')) 
#replace GRÜNE/B 90 by 'GRÜNE' and ÖDP / Familie by 'ÖDP'
ds['gruppe'] = ds['gruppe'].replace(to_replace = ['GRÜNE/B 90','ÖDP / Familie '], value = ['GRÜNE','ÖDP'])

#seperate valid_votes from data frame
votes_total = ds[ds['gruppe'] == 'Gültige']['zweitstimmen'].sum()
ds = ds[ds['gruppe'] != 'Gültige'].reset_index(drop = True)

#%%
#Task 1

#Method of Sainte-Lague/Schepers
def SLS(seats,seats_total,divisor,votes):
    while seats.sum() != seats_total:
        if seats.sum() > seats_total:
            divisor += 1
        elif seats.sum() < seats_total:
            divisor -=1
            
        seats = round(votes / divisor)
    return (seats,divisor)

#%%
#Task 2

#find winners of 'erststimmen' and sort them by 'wahlkreis'
votes1 = ds.loc[ds.reset_index().groupby(['wahlkreis'])['erststimmen'].idxmax()].sort_values(by = 'wahlkreis').reset_index(drop = True)

#count 'wahlkreis' for each party per state
votes1_state = votes1.groupby(['land','gruppe'])['erststimmen'].sum().reset_index()
votes1_state['wahlkreis'] = votes1.groupby(['land','gruppe'])['erststimmen'].count().reset_index()['erststimmen']

#%%
#Task 3

#distribution of seats by states according to the population

#importing the dataset into data frame
#state;name;population
ds_pop = pd.read_csv('population.csv', delimiter=';')

states_seats = ds_pop[['state','name','population']].sort_values(by = 'state').reset_index(drop = True)
           
#total number of seats
seats_total = 598
#calculation of distribution         
divisor = round(states_seats['population'].sum() / seats_total)
states_seats['seats'],divisor = SLS(round(states_seats['population'] / divisor) , seats_total, divisor, states_seats['population']) 

#name instead of number in 'land'
votes1_state['land'] = states_seats['name'][votes1_state['land']-1].values
votes1_state = votes1_state.sort_values(by = ['land','gruppe'], ascending = True).reset_index(drop = True)

#%%
#Task 4

#parties in parlament
#sum up 'zweitstimmen' by party
votes2_parla = ds.groupby(['gruppe'])['zweitstimmen'].sum().reset_index()

#drop data with 0 zweitstimmen
votes2_parla = votes2_parla[votes2_parla['zweitstimmen']> 0]
#drop parties with zweitstimmen < 5%
votes2_parla = votes2_parla[(votes2_parla['zweitstimmen'] / votes_total)  >= 0.05]
#sort parties by zweitstimmen
votes2_parla = votes2_parla.sort_values(by = 'zweitstimmen', ascending = False).reset_index(drop = True)

#parties in parlament by state
#sum up 'zweitstimmen' by party per state
votes2_state = ds.groupby(['land','gruppe'])['zweitstimmen'].sum().reset_index()
#drop parties with < 5% in total
votes2_state = votes2_state[votes2_state['gruppe'].isin(votes2_parla['gruppe'])]
#sort parties by zweitstimmen
votes2_state = votes2_state.sort_values(by = ['land','gruppe'], ascending = True).reset_index(drop = True)

#get ranges of states as indices
ui = np.unique(votes2_state['land'], return_index = True)
ui = list(ui[1])
ui.append(votes2_state.shape[0])
   
#calculate seat distribution
votes2_state['seats'] = 0
for i in range(0,votes2_state['land'].max()):
    divisor = round(votes2_state['zweitstimmen'][ui[i]:ui[i+1]].sum() / states_seats['seats'][i])   #seats XXXXXX -> xx
    votes2_state.loc[ui[i]:ui[i+1],'seats'],d = SLS(round(votes2_state['zweitstimmen'][ui[i]:ui[i+1]] / divisor), states_seats['seats'][i], divisor, votes2_state['zweitstimmen'][ui[i]:ui[i+1]]) #states_seats['population'])
    
#%%
#Task5

#create final result as csv output
result = pd.DataFrame()
result['state'] = states_seats['name'][votes2_state['land']-1]
result = result.reset_index(drop = True)
result['party'] = votes2_state['gruppe'].values
result['direct_seats'] = 0
result['list_seats'] = votes2_state['seats'].astype(int)
result['ueberhang'] = 0

#copy direct seats and calculate ueberhang
for i in range(0,len(result)):
    for j in range(0,len(votes1_state)):
        if (result['state'][i] == votes1_state['land'][j]) and (result['party'][i] == votes1_state['gruppe'][j]):
            result.loc[i,'direct_seats'] = votes1_state['wahlkreis'][j]
            result.loc[i,'ueberhang'] = max(result['direct_seats'][i] - result['list_seats'][i],0)
            break
    
#sort result and put it out
result = result.sort_values(by = ['state','party'], ascending = True).reset_index(drop = True)

print(result.to_csv(sep = ';',index = False))

#save as csv file
#print(result.to_csv(path_or_buf = 'result3.csv',sep = ';',index = False))