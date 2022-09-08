

import pandas as pd
import math
from copy import deepcopy

df = pd.read_csv(r'C:\Users\angus\OneDrive\Desktop\FPL\fpl22\dataset_with_roles.csv')
df = df.set_index(['Player', 'Gameweek'])
df.columns


df['Goal prob'] = 1 / df['Goal odds']
df['Assist prob'] = 1 / df['Assist odds']

#creating a midfielder dataframe
df1 = df[df['Role'] == 3]
df1['Goal imputed'], df1['Assist imputed'] = 0, 0

df2 = deepcopy(df1)


def impute_def(player, gw, df1, df2):
    
    #if we don't have 'CS odds' we don't do imputation
    if (math.isnan(df1.loc[(player, gw), 'Assist odds'])) and \
        (not math.isnan(df1.loc[(player, gw), 'Goal odds'])):
        
        #Computing the value to impute for 'CS prob'
        indices_to_use = (df1.loc[player].loc[:gw-1]['Assist odds'].notna()) & \
                    (df1.loc[player].loc[:gw-1]['Goal odds'].notna())
        valid_rows_df = df1.loc[player].loc[:gw-1][indices_to_use]
        avg_assist_prob = valid_rows_df['Assist prob'].mean()
        avg_goal_prob = valid_rows_df['Goal prob'].mean()
        #intuitive formula for 'Goal prob' imputation
        imputed_assist_prob = df1.loc[(player, gw), 'Goal prob'] / avg_goal_prob * \
                            avg_assist_prob
        
       
        #adding the imputed values to the second copy 'df2'
        df2.loc[(player, gw), ['Assist prob', 'Assist imputed']] = \
            [imputed_assist_prob, 1]
    
    elif (not math.isnan(df1.loc[(player, gw), 'Assist odds'])) and \
        (math.isnan(df1.loc[(player, gw), 'Goal odds'])):
        
        #Computing the value to impute for 'CS prob'
        indices_to_use = (df1.loc[player].loc[:gw-1]['Assist odds'].notna()) & \
                    (df1.loc[player].loc[:gw-1]['Goal odds'].notna())
        valid_rows_df = df1.loc[player].loc[:gw-1][indices_to_use]
        avg_assist_prob = valid_rows_df['Assist prob'].mean()
        avg_goal_prob = valid_rows_df['Goal prob'].mean()
        #intuitive formula for 'Goal prob' imputation
        imputed_goal_prob = df1.loc[(player, gw), 'Assist prob'] / avg_assist_prob * \
                            avg_goal_prob
        
       
        #adding the imputed values to the second copy 'df2'
        df2.loc[(player, gw), ['Goal prob', 'Goal imputed']] = \
            [imputed_goal_prob, 1]
    
            
for player, gw in df1.index:
    impute_def(player, gw, df1, df2)
    
        
        
df3 = deepcopy(df2)      
df3.to_csv(r'C:\Users\angus\OneDrive\Desktop\FPL\fpl22\forwards_full_df.csv')      
df4 = df3[(df3['Minutes'] > 60)  & (df3['Goal prob'].notna()) & (df3['Assist prob'].notna())]    
df4.to_csv(r'C:\Users\angus\OneDrive\Desktop\FPL\fpl22\forwards_cleaned_df.csv') 
df5 = df4.iloc[:, 5:8].dropna()
df5.to_csv(r'C:\Users\angus\OneDrive\Desktop\FPL\fpl22\forwardss_regression_df.csv')


import matplotlib.pyplot as plt
plt.figure()
plt.plot(df2.loc['Kane']['Goal prob'], df2.loc['Kane']['Assist prob'], 'bo')    
plt.plot(df2.loc['Dennis']['Goal prob'], df2.loc['Dennis']['Assist prob'], 'ro')   
