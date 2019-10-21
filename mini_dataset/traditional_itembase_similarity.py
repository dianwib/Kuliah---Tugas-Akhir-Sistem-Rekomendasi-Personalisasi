from __future__ import division
import pandas as pd
import numpy as np
data=pd.read_csv("matrix_s.csv",dtype=float)
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

        atas+=data.at[user,item_a]*data.at[user,item_b]
        l_atas.append(data.at[user,item_a]*data.at[user,item_b])

        bawah_kiri+=data.at[user,item_a]**2
        l_bawah_kiri.append(data.at[user,item_a]**2)

        bawah_kanan += data.at[user, item_b] ** 2
        l_bawah_kanan.append(data.at[user, item_b] ** 2)
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


print(data_2)
data_2.to_csv("traditional_matrix_similaritas_item.csv")