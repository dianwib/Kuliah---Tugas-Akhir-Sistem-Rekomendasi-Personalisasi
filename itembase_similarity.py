import pandas as pd
import numpy as np
data=pd.read_csv("matrix_rating_3.csv")
data_2=pd.DataFrame(data,index=np.array(1-944),columns=np.array(1-1683))

del data['Unnamed: 0']
del data['User']
input_user=int(input("masukkan user target"))
print(data.columns)

temp_item_kosong=0
for item in (data.columns):
    if
