

import pandas as pd
import math
from copy import deepcopy

df = pd.read_csv(r'C:\Users\angus\OneDrive\Desktop\FPL\fpl22\dataset_with_roles.csv')
df = df.set_index(['Player', 'Gameweek'])
df.columns


df['Goal prob'] = 1 / df['Goal odds']
df['Assist prob'] = 1 / df['Assist odds']
df['CS prob'] = 1 / df['CS odds']

#creating a midfielder dataframe
df1 = df[df['Role'] == 2]
df1['Goal imputed'], df1['Assist imputed'], df1['CS imputed'] = 0, 0, 0

df2 = deepcopy(df1)


'''df2.loc['Alonso'].loc[2:5][math.isnan(df2.loc['Alonso'].loc[2:5]['CS odds'])]
type(df2.loc['Alonso'].loc[2:5]['Goal odds'])
indices_to_use = df2.loc['Alonso'].loc[2:5]['Goal odds'].isna()

indices_to_use = (df2.loc[player].loc[:gw]['CS odds'].notna()) & \
                    (df2.loc[player].loc[:gw]['Goal odds'].notna())

player = 'Alonso'
gw = 7
df2.loc[player].loc[:gw]'''

def impute_def(player, gw, df1, df2):
    
    #if we don't have 'CS odds' we don't do imputation
    if (math.isnan(df1.loc[(player, gw), 'CS odds'])) and \
        (not math.isnan(df1.loc[(player, gw), 'Goal odds'])) and \
    (math.isnan(df1.loc[(player, gw), 'Assist odds'])):
        
        #Computing the value to impute for 'CS prob'
        indices_to_use = (df1.loc[player].loc[:gw-1]['CS odds'].notna()) & \
                    (df1.loc[player].loc[:gw-1]['Goal odds'].notna())
        valid_rows_df = df1.loc[player].loc[:gw-1][indices_to_use]
        avg_cs_prob = valid_rows_df['CS prob'].mean()
        avg_goal_prob = valid_rows_df['Goal prob'].mean()
        #intuitive formula for 'Goal prob' imputation
        imputed_cs_prob = df1.loc[(player, gw), 'Goal prob'] / avg_goal_prob * \
                            avg_cs_prob
        
            
        #Same thing as above but for 'Assist prob' imputation
        
        indices_to_use = (df1.loc[player].loc[:gw-1]['GOal odds'].notna()) & \
                    (df1.loc[player].loc[:gw-1]['Assist odds'].notna())
        valid_rows_df = df1.loc[player].loc[:gw-1][indices_to_use]
        avg_goal_prob = valid_rows_df['Goal prob'].mean()
        avg_assist_prob = valid_rows_df['Assist prob'].mean()
        imputed_assist_prob = df1.loc[(player, gw), 'Goal prob'] / avg_goal_prob * \
                            avg_assist_prob
        
        #adding the imputed values to the second copy 'df2'
        df2.loc[(player, gw), ['CS prob', 'Assist prob', 'CS imputed', 'Assist imputed']] = \
            [imputed_cs_prob, imputed_assist_prob, 1, 1]
            
    elif (math.isnan(df1.loc[(player, gw), 'CS odds'])) and \
        (not math.isnan(df1.loc[(player, gw), 'Goal odds'])) and \
    (not math.isnan(df1.loc[(player, gw), 'Assist odds'])):
        
        #Computing the value to impute for 'CS prob'
        indices_to_use = (df1.loc[player].loc[:gw-1]['CS odds'].notna()) & \
                    (df1.loc[player].loc[:gw-1]['Goal odds'].notna())
        valid_rows_df = df1.loc[player].loc[:gw-1][indices_to_use]
        avg_cs_prob = valid_rows_df['CS prob'].mean()
        avg_goal_prob = valid_rows_df['Goal prob'].mean()
        #intuitive formula for 'Goal prob' imputation
        imputed_cs_prob = df1.loc[(player, gw), 'Goal prob'] / avg_goal_prob * \
                            avg_cs_prob
        
        #adding the imputed values to the second copy 'df2'
        df2.loc[(player, gw), ['CS prob', 'CS imputed']] = \
            [imputed_cs_prob, 1]
        
        
    
    elif (not math.isnan(df1.loc[(player, gw), 'CS odds'])) and \
    (math.isnan(df1.loc[(player, gw), 'Goal odds'])) and \
    (math.isnan(df1.loc[(player, gw), 'Assist odds'])):
        
        #Computing the value to impute for 'Goal prob'
        
        #Series of booleans of len 'gw' that tells you which rows to use
        #Remark when you use .loc[:gw] it works as .iloc so to discard gw row
        #you need to use :gw-1
        indices_to_use = (df1.loc[player].loc[:gw-1]['CS odds'].notna()) & \
                    (df1.loc[player].loc[:gw-1]['Goal odds'].notna())
        #Creating a small dataframe with the valid rows
        valid_rows_df = df1.loc[player].loc[:gw-1][indices_to_use]
        avg_cs_prob = valid_rows_df['CS prob'].mean()
        avg_goal_prob = valid_rows_df['Goal prob'].mean()
        #intuitive formula for 'Goal prob' imputation
        imputed_goal_prob = df1.loc[(player, gw), 'CS prob'] / avg_cs_prob * \
                            avg_goal_prob
                            
        #Same thing as above but for 'Assist prob' imputation
        
        indices_to_use = (df1.loc[player].loc[:gw-1]['CS odds'].notna()) & \
                    (df1.loc[player].loc[:gw-1]['Assist odds'].notna())
        valid_rows_df = df1.loc[player].loc[:gw-1][indices_to_use]
        avg_cs_prob = valid_rows_df['CS prob'].mean()
        avg_assist_prob = valid_rows_df['Assist prob'].mean()
        imputed_assist_prob = df1.loc[(player, gw), 'CS prob'] / avg_cs_prob * \
                            avg_assist_prob
        
        #adding the imputed values to the second copy 'df2'
        df2.loc[(player, gw), ['Goal prob', 'Assist prob', 'Goal imputed', 'Assist imputed']] = \
            [imputed_goal_prob, imputed_assist_prob, 1, 1]
            
    elif (not math.isnan(df1.loc[(player, gw), 'CS odds'])) and \
    (math.isnan(df1.loc[(player, gw), 'Goal odds'])) and \
    (not math.isnan(df1.loc[(player, gw), 'Assist odds'])):
        
        #Computing the value to impute for 'Goal prob'
        
        #Series of booleans of len 'gw' that tells you which rows to use
        #Remark when you use .loc[:gw] it works as .iloc so to discard gw row
        #you need to use :gw-1
        indices_to_use = (df1.loc[player].loc[:gw-1]['Assist odds'].notna()) & \
                    (df1.loc[player].loc[:gw-1]['Goal odds'].notna())
        #Creating a small dataframe with the valid rows
        valid_rows_df = df1.loc[player].loc[:gw-1][indices_to_use]
        avg_assist_prob = valid_rows_df['Assist prob'].mean()
        avg_goal_prob = valid_rows_df['Goal prob'].mean()
        #intuitive formula for 'Goal prob' imputation
        imputed_goal_prob = df1.loc[(player, gw), 'Assist prob'] / avg_assist_prob * \
                            avg_goal_prob
                            
        
        #adding the imputed values to the second copy 'df2'
        df2.loc[(player, gw), ['Goal prob', 'Goal imputed']] = \
            [imputed_goal_prob, 1]
            
    elif (not math.isnan(df1.loc[(player, gw), 'CS odds'])) and \
    (not math.isnan(df1.loc[(player, gw), 'Goal odds'])) and \
    (math.isnan(df1.loc[(player, gw), 'Assist odds'])):
        
        #Same thing as above but for 'Assist prob' imputation
        
        indices_to_use = (df1.loc[player].loc[:gw-1]['Goal odds'].notna()) & \
                    (df1.loc[player].loc[:gw-1]['Assist odds'].notna())
        valid_rows_df = df1.loc[player].loc[:gw-1][indices_to_use]
        avg_goal_prob = valid_rows_df['Goal prob'].mean()
        avg_assist_prob = valid_rows_df['Assist prob'].mean()
        imputed_assist_prob = df1.loc[(player, gw), 'Goal prob'] / avg_goal_prob * \
                            avg_assist_prob
        
        #adding the imputed values to the second copy 'df2'
        df2.loc[(player, gw), ['Assist prob', 'Assist imputed']] = \
            [imputed_assist_prob, 1]
            
for player, gw in df1.index:
    impute_def(player, gw, df1, df2)
    
        
        
df3 = deepcopy(df2)      
df3.to_csv(r'C:\Users\angus\OneDrive\Desktop\FPL\fpl22\midfielders_full_df.csv')      
df4 = df3[(df3['Minutes'] > 60) & (df3['CS prob'].notna()) & (df3['Goal prob'].notna()) & (df3['Assist prob'].notna())]    
df4.to_csv(r'C:\Users\angus\OneDrive\Desktop\FPL\fpl22\midfielders_cleaned_df.csv') 
df5 = df4.iloc[:, 5:9].dropna()
df5.to_csv(r'C:\Users\angus\OneDrive\Desktop\FPL\fpl22\midfielders_regression_df.csv')


import matplotlib.pyplot as plt
plt.figure()
plt.plot(df2.loc['Mané']['Goal prob'], df2.loc['Mané']['Assist prob'], 'bo')    
plt.plot(df2.loc['Mahrez']['Goal prob'], df2.loc['Mahrez']['Assist prob'], 'ro')   
