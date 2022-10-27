import pandas as pd
import numpy as np

def get_team_score(team_number):
    final_table_columns = ['name', 'earned']

    port = "3{}".format(str(team_number).rjust(3, '0')) # pad team number as 3XXX

    try: 
        # get data
        url = "http://localhost:{}/api/Challenges".format(port)
        df = pd.read_json(url)

        # flatten json
        df = pd.json_normalize(df['data'])

        # drop challenges that can't work in Docker
        df.drop(df[df['disabledEnv'] == "Docker"].index, inplace=True)

        # calculate points earned (by solved = true)
        df['earned'] = df['difficulty'] * df['solved']

        # drop unneeded columns 
        df = df[df.columns.intersection(final_table_columns)]

    except:
        df = pd.DataFrame()

    # drop challenges due to Docker limitation
    

    # add team number
    df.insert(0, 'team', team_number)

    return df

# df_final = pd.concat([df_final, get_team_score(2)])
# df_final = pd.concat([df_final, get_team_score(3)])
# df_final = pd.concat([df_final, get_team_score(4)])
#print(get_team_score(3))

def get_all_team_scores(start,end):
    df_final = pd.DataFrame()

    for team_number in range(1, end + 1):
        df_final = pd.concat([df_final, get_team_score(team_number)])
    return df_final


#print(df_final)

def pretty_table(df_final):
    table = pd.pivot_table(df_final, values='earned', index=['team'],
        columns=[ 'name'], aggfunc=np.sum, fill_value=0)
    table['Sum'] = table.sum(axis=1, numeric_only=True)
    table = table.transpose()
    table['ChallengeSum'] = table.sum(axis=1, numeric_only=True)
    #print(table)


    # table.transpose().to_html('tempv.html')
    # table.to_html('temph.html')


    # Only show completed challenges that have points
    table_limited = (table[table['ChallengeSum'] > 0]).loc[:, table.columns!='ChallengeSum']
    #print(table_limited.transpose().to_html)
    return table_limited.to_html()

if __name__ == "__main__":
    print(pretty_table(get_all_team_scores(1,4)))