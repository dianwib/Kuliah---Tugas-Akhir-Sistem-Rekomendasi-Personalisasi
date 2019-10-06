import pandas as pd
import numpy as np
data=pd.read_csv("matrix_rating_3.csv")
del data['Unnamed: 0']
del data['User']
data_2=data
for user in data.index:
    print(user)
    temp_nilai_total_user=data.sum(axis=1,skipna=True)
    for item in data.columns:
        nilai_matrix_lama=float(data.at[user,item])
        data_2.at[user,item]=nilai_matrix_lama/temp_nilai_total_user[user]

data_2.to_csv("matrix_s.csv")