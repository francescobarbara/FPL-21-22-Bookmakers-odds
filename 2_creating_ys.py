
d = {
     'Alonso':
         {'role' : 1,
     'url' : '',
     'valid_gws' : [i for i in range(1, 39)]},
    
     
     'Salah':
    {'role' : 2,
     'url' : 'https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2021-22/players/Mohamed_Salah_233/gw.csv',
     'valid_gws' : [i for i in range(1, 39)]},
    
    }


df2 = deepcopy(df)
#creating a multi-index (player, gameweek)
df3 = df2.set_index(['Player', 'Gameweek'])

all_players_rows = []

for player in d.keys():
    player_rows = []
    role, url, gws = d[player]['role'], d[player]['url'], d[player]['valid_gws']
    
    #retrieving vastaav's data for the specific player
    fpl_stats = pd.read_csv(url)
    for gw in gws:
        #these are the xs (covariates)
        row = [player, gw, df3.loc[(player, gw), 'Goal odds'], 
               df3.loc[(player, gw), 'Assist odds'], 
               df3.loc[(player, gw), 'CS odds'],
               fpl_stats.loc[gw-1, 'minutes'],
               fpl_stats.loc[gw-1, 'total_points']]
        player_rows.append(row)
        
    all_players_rows = all_players_rows + player_rows
    
type(df3.loc[('Alonso', 1)])

gw = 1
fpl_stats.loc[gw-1, 'minutes'] 