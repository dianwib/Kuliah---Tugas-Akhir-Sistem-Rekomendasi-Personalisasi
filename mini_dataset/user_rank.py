import pandas as pd
import numpy as np
import math

data = pd.read_csv("matrix_cm.csv")
data_2 = pd.DataFrame(index=np.arange(1,6))
del data['Unnamed: 0']
data.index = pd.RangeIndex(start=1, stop=6, step=1)
data.columns = [1, 2, 3, 4, 5]
data_2[0] = 0.2

#print(data)
#print(data_2)
list_uk={}
for user_n in(data.index):
    #print(user_n)
    temp = 0
    uk = []
    for user_k in (data.columns):
        #print(user_k)
        #print(data.at[user_n,user_k])
        if data.at[user_n,user_k] > 0:
            temp+=1
            uk.append(user_k)
    list_uk[user_n] = uk
#print(list_uk)

alfa = 0.5
kolom_iterasi = 0
nilai_error = 0.004
ketemu = False
while not ketemu:
    print("Iterasi ke : ", kolom_iterasi+1)
    for user in data.index:
        #print('user',user)
        #print(list_uk[user])
        temp = 0
        print("UR User : ", user)
        for out_user in list_uk[user]:
            #print(out_user)
            temp += data_2.at[out_user,kolom_iterasi] * data.at[out_user,user]
            print("data uk : ", data_2.at[out_user,kolom_iterasi], "data cm : ", data.at[out_user, user], "hasil uk*cm : ", temp)
            #print(temp)
        #print(data_2.at[user, kolom_iterasi])
        hasil = ((1-alfa)*data_2.at[user,kolom_iterasi])+(alfa*temp)
        print("data un : ", data_2.at[user,kolom_iterasi],"hasil ur : ", hasil)

        data_2.at[user, kolom_iterasi+1] = hasil
    #print(data_2)
    
    #print(data_2.sum(axis=0))
    #if data_2.sum(axis=0)
    batas = 0
    for user_rank in data_2.index:
        batas += data_2.at[user_rank,kolom_iterasi+1] - data_2.at[user_rank,kolom_iterasi]
        #print(batas)
    selisih_error = math.fabs(batas)/len(data_2.index)
    #print(selisih_error)
    if selisih_error < nilai_error :
        ketemu = True
        data_2.to_csv('matrix_user_rank.csv')
    else :
        kolom_iterasi+=1
        
    

        
        
