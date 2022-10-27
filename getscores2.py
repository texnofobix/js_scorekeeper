import pandas as pd
import numpy as np

df_final = pd.DataFrame()
final_table_columns = ['name', 'earned']

#########
url = "http://localhost:3003/api/Challenges"
df = pd.read_json(url)
# print(df)

# flatten json
df = pd.json_normalize(df['data'])
# print(df)


# drop challenges due to Docker limitation
df.drop(df[df['disabledEnv'] == "Docker"].index, inplace=True)
# print(df)
df['earned'] = df['difficulty'] * df['solved']


df = df[df.columns.intersection(final_table_columns)]
# print(df)



df.insert(0, 'team', 3)
# print(df)
#print(df['earned'].sum())

df_final = pd.concat([df_final, df])
# df = df.drop(df[df['disabledEnv'] == "Docker"].index, inplace=False)

# url = "http://localhost:3004/api/Challenges"
# df += pd.read_json(url)
# print(df)\
print('total', df['earned'].sum())

##########


url = "http://localhost:3004/api/Challenges"
df = pd.read_json(url)
# print(df)

# flatten json
df = pd.json_normalize(df['data'])
# print(df)

# drop challenges due to Docker limitation
df.drop(df[df['disabledEnv'] == "Docker"].index, inplace=True)
# print(df)
df['earned'] = df['difficulty'] * df['solved']

df = df[df.columns.intersection(final_table_columns)]
# print(df)



df.insert(0, 'team', 4)
# print(df)
print('total', df['earned'].sum())

df_final = pd.concat([df_final, df])


print(df_final)


table = pd.pivot_table(df_final, values='earned', index=['team'],
    columns=[ 'name'], aggfunc=np.sum, fill_value=0)
print(table)


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
#pd.set_option('display.width', 1000)
# pd.set_option('display.colheader_justify', 'center')
pd.set_option('display.precision', 0)

table['Sum'] = df.sum(axis=1, numeric_only=True)
print(table.)