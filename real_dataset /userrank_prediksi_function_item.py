from __future__ import division
import pandas as pd
import numpy as np
data=pd.read_csv("userrank_matrix_similaritas_item.csv")
data_2=pd.read_csv("matrix_rm.csv")
import math
print(data)
del data_2['Unnamed: 0']
#ganti colom as index
data.set_index('Unnamed: 0',inplace=True)

data_2.index=pd.RangeIndex(start=1, stop=6,step=1) # re index

print(data)
print(data_2)
#print(data.columns)
#print(data.index)

#print(data_2.columns)
#print(data_2.index)

input_k=int(input("masukkan k: "))
input_top_N=int(input("masukkan jumlah top N: "))

#cari tetangga

def cari_tetangga(item_target,banyak_tetangga):
    #for item_target in data.index:
    temp_per_item_target = data.loc[item_target]  # select per index
    temp_per_item_target.sort_values(ascending=False, inplace=True)  # sorting desc
    temp_per_item_target = temp_per_item_target.iloc[:banyak_tetangga]  # spit berdasarkan max k
    print(temp_per_item_target)
    list_QtU_item_k = temp_per_item_target.index.tolist()  # get index/item dari data stlh disorting convert ke list
    print(list_QtU_item_k)

    return list_QtU_item_k


def hitung_function(user_target,item_target,list_item_similar_qtu):
    atas=0.0
    bawah=0.0
    #print(data_2.index)
    #print(data.index)

    for item_similar in list_item_similar_qtu:
        #print(item_similar,item_target)
        #print(data.at[item_target,item_similar])
        atas+=data.at[item_target,item_similar] * data_2.at[user_target,item_similar]
        bawah+=math.fabs(data.at[item_target,item_similar])
        print("similaritas item(",item_target, item_similar,")= ",data.at[item_target, item_similar]," * rating user item(",user_target, item_similar,")= " , data_2.at[user_target, item_similar])
        print("absolute similaritas item(",item_target, item_similar,")= ",math.fabs(data.at[item_target, item_similar]))
    hasil=float(atas)/float(bawah)
    print(hasil)
    return hasil

##statis
user_target=1

data_hasil=pd.DataFrame(data,index=data.index,columns=['Nilai'])

print(data_hasil.index)
for item_target in data.index:
    QtU=cari_tetangga(item_target,input_k)
    hasil=hitung_function(user_target,item_target,QtU)
    data_hasil.at[item_target,'Nilai']=hasil
    print("item > ",item_target,": ",hasil)
data_hasil.to_csv("userrank_matrix_prediksi.csv")
print(data_hasil)

data_top_n=data_hasil.sort_values(ascending=False, inplace=True,by=['Nilai'])  # sorting desc
data_top_n = data_hasil.iloc[:input_top_N]  # spit berdasarkan max top n
data_top_n.to_csv("userrank_matrix_top_n.csv")
print("top N>>>>>>>>>>>>>>>\n",data_top_n)