from __future__ import division
import pandas as pd
import numpy as np
data_userrank=pd.read_csv("matrix_user_rank.csv")
data_userrank.set_index('Unnamed: 0',inplace=True)
data=pd.read_csv("matrix_s.csv",dtype=float)

print(data_userrank)
import math
del data['Unnamed: 0']
input_user=int(input("masukkan user target"))
data.index=pd.RangeIndex(start=1, stop=len(data.index)+1,step=1)

temp_item_kosong=[]
temp_item_terisi=[]
data_2=pd.DataFrame(dtype=float)

for item in (data.columns):
    if data.at[input_user,item] == 0.0:
        temp_item_kosong.append(item)
    else:
        temp_item_terisi.append(item)

print(temp_item_kosong)
print(len(temp_item_kosong))

def cari_user(item_a, item_b):
    irisan_user_pada_item_a_b = []
    for user in data.index:
        if user != input_user:
            if data.at[user, item_a] != 0.0 and data.at[user, item_b] != 0.0:
                irisan_user_pada_item_a_b.append(user)
        else:
            continue
    print("user yang merating item ",item_a,item_b,": user ",irisan_user_pada_item_a_b)
    return irisan_user_pada_item_a_b


def hitung_similarity(item_a,item_b,list_irisan_a_b):
    atas=0
    bawah_kiri=0
    bawah_kanan=0
    l_atas=[]
    l_bawah_kiri=[]
    l_bawah_kanan=[]
    for user in list_irisan_a_b:
        kolom_terakhir=(data_userrank.columns[-1])
        print("pagerank user", user, "= ", data_userrank.at[user, kolom_terakhir],"**2:",data_userrank.at[user, kolom_terakhir]**2)

        atas+=data.at[user,item_a]*data.at[user,item_b] * (data_userrank.at[user,kolom_terakhir]**2) #str karena tipe data kolom pagerank adlh string
        l_atas.append(data.at[user,item_a]*data.at[user,item_b]*(data_userrank.at[user,kolom_terakhir]**2))
        print("similaritas ",user,item_a,":",data.at[user,item_a],"dan",user,item_b,":",data.at[user,item_b] ,"userrank",user,":", (data_userrank.at[user,kolom_terakhir]**2))

        bawah_kiri+=(data.at[user,item_a]**2) *(data_userrank.at[user,kolom_terakhir]**2)
        l_bawah_kiri.append((data.at[user,item_a]**2) *(data_userrank.at[user,kolom_terakhir]**2))
        print("similaritas ", user, item_a, ":", data.at[user, item_a]**2, "userrank", user, ":", data_userrank.at[user, kolom_terakhir])

        bawah_kanan += (data.at[user, item_b] ** 2) *(data_userrank.at[user,kolom_terakhir]**2)
        l_bawah_kanan.append((data.at[user, item_b] ** 2) *(data_userrank.at[user,kolom_terakhir]**2))
        print("similaritas ", user, item_b, ":", data.at[user, item_b] ** 2, "userrank", user, ":",
              data_userrank.at[user, kolom_terakhir])

    bawah=(math.sqrt(bawah_kiri)) * (math.sqrt(bawah_kanan))
    hasil=float(atas / bawah)
    print("sum atas ",l_atas)
    print("sum bawah kiri ",l_bawah_kiri)
    print("sum bawah kanan ",l_bawah_kanan)
    print("atas ", atas)
    print("bawah kiri ", math.sqrt(bawah_kiri))
    print("bawah kanan ", math.sqrt(bawah_kanan))
    print("bawah ", bawah)
    print("similaritas ",item_a,item_b)
    print("hasil",hasil,">>>>>>>>>>>\n")
    return hasil


for item_target in temp_item_kosong:
    for item_pembanding in temp_item_terisi:
        list_irisan_a_b=cari_user(item_target,item_pembanding)
        if len(list_irisan_a_b)==0:
            continue
        else:
            data_2.at[item_target,item_pembanding]=hitung_similarity(item_target,item_pembanding,list_irisan_a_b)


data_2.to_csv("userrank_matrix_similaritas_item.csv")