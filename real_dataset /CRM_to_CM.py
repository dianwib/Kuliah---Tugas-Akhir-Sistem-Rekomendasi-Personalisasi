import pandas as pd
import numpy as np

data = pd.read_csv('matrix_CRM.csv')
data_2 = pd.DataFrame( columns = np.arange(1, len(data.index)+1))
del data['Unnamed: 0']

##c = data.sum(axis = 1, skipna = True)
##print(c)


#data.set_index('Unnamed: 0.1',inplace =True)
print(data_2.columns)
for i in data.index:
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

data_2.to_csv('matrix_CM.csv')
         