import pandas as pd
import numpy as np

data = pd.read_csv('matrix_rating_4.csv')
data_2 = pd.DataFrame( columns = np.arange(1, 944))
del data['Unnamed: 0']

##c = data.sum(axis = 1, skipna = True)
##print(c)
print(data_2.columns)
for i in range(943):
    c = data.sum(axis=1, skipna = True)
    #a = []
    print (i)
    for j in data.columns:
        if data.at[i, j] > 0 :
            #print(data.at[i,j])
            data_lama = data.at[i,j]
            #print(data_lama)
            data_baru = data_lama/c[i]
            #print(c[i])
            #print(data_baru)

            data_2.at[i, int(j)]=data_baru

data_2.to_csv('matrix_rating_5.csv')
            #a.append(data_baru)
##        else:
##            data.at[i,j].fillna(0.0, inplace=True)
        
#print(c)
#print(a)

