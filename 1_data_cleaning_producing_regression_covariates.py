# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 16:32:34 2022

@author: angus
"""

import pandas as pd
from copy import deepcopy

data = pd.read_excel(r'C:\Users\angus\OneDrive\Desktop\FPL\fpl22\odds22.xlsx', index_col = 0, header = None)
#Using this trick so that columns of gameweeks present in 2021 and 2022 do not
#get a weird suffix

#Removing 2021 columns
data = data.iloc[:,30:]
#changing column names (as we did not use header = 0 at the start)
data.columns = data.iloc[0,:]
#Removing the header row
data = data.iloc[1:,:]

#copying the dataset as a back-up
data2 = deepcopy(data) 
#make a player name column
data3 = data2.reset_index(level=0)
data3.rename(columns={0:'Player'}, inplace=True)

nrows, ncols = data.shape
ncols = ncols//3 #i.e. ncols = 38

#Creating the list to feed pd.DataFrame()
l = []
for player in range(nrows):
    for gw in range(ncols):
        row = [data3.iloc[player, 0], gw + 1, data3.iloc[player, 3*gw + 1], 
               data3.iloc[player, 3*gw + 2], data3.iloc[player, 3*gw + 3] ]
        l.append(row)
    
df = pd.DataFrame(l)
df.columns = ['Player', 'Gameweek', 'Goal odds', 'Assist odds', 'CS odds']
df.to_csv(r'C:\Users\angus\OneDrive\Desktop\FPL\fpl22\regression_covariates.csv')



