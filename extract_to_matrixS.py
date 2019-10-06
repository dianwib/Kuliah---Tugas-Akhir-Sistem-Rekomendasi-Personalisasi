import pandas as pd
import numpy as np
data=pd.read_csv("matrix_rating_3.csv")
del data['Unnamed: 0']
del data['User']
data_2=data

print(data.columns)

for user in data.index:
    temp_nilai_total_user=data.sum(axis=1,skipna=True)
    for item in data.columns:
        data_2.at[user,item]=data.at[user,item]/temp_nilai_total_user

data_2.to_csv("matrix_s.csv")