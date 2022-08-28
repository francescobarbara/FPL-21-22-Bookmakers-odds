
d = {
     'Alonso':
         {'role' : 1,
     'url' : 'https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2021-22/players/Mohamed_Salah_233/gw.csv',
     'valid_gws' : [i for i in range(1, 39)]},
    
     
     'Salah':
    {'role' : 2,
     'url' : 'https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2021-22/players/Mohamed_Salah_233/gw.csv',
     'valid_gws' : [i for i in range(1, 39)]}
    
    }


df2 = deepcopy(df)
#creating a multi-index (player, gameweek)
df3 = df2.set_index(['Player', 'Gameweek'])



def modify_round(fpl_stats):
    #since often times you have double gameweeks (for ex. Salah has two rows)
    #where round variable is 26, we modify to guarantee uniqueness and consistency
    #with the Norwegian data
    gws = fpl_stats.shape[0]
    fpl_stats['round'] = pd.Series(range(39 - gws, 39))
    fpl_stats = fpl_stats.set_index('round')
    return fpl_stats



all_players_rows = []

for player in d.keys():
    player_rows = []
    role, url, gws = d[player]['role'], d[player]['url'], d[player]['valid_gws']
    
    #retrieving vastaav's data for the specific player
    fpl_stats = pd.read_csv(url)
    fpl_stats = modify_round(fpl_stats)
    for gw in gws:

        try:
            row = [player, gw, role, df3.loc[(player, gw), 'Goal odds'], 
                   df3.loc[(player, gw), 'Assist odds'], 
                   df3.loc[(player, gw), 'CS odds'],
                   fpl_stats.loc[gw, 'minutes'],
                   fpl_stats.loc[gw, 'total_points']]
            player_rows.append(row)
        except:
            print(player, gw, 'issue with this gameweek')
    all_players_rows = all_players_rows + player_rows
    
final_df = pd.DataFrame(all_players_rows)
final_df.columns = ['Player', 'Gameweek', 'Role', 'Goal odds', 'Assist odds', 'CS odds', 'Minutes', 'Points']
final_df = final_df.set_index(['Player', 'Gameweek'])
final_df.to_csv(r'C:\Users\angus\OneDrive\Desktop\FPL\fpl22\dataset_with_roles.csv')
