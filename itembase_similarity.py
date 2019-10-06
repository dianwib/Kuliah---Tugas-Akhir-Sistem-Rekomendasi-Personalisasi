from __future__ import division
import pandas as pd
import numpy as np
data=pd.read_csv("matrix_s.csv")
import math
del data['Unnamed: 0']
input_user=int(input("masukkan user target"))
input_user=input_user-1
temp_item_kosong=[]
temp_item_terisi=[]
data_2=pd.DataFrame(data,index=np.array(1-1683),columns=np.array(1-1683))

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
                irisan_user_pada_item_a_b.append(user + 1)

        else:
            continue
    print(irisan_user_pada_item_a_b)
    return irisan_user_pada_item_a_b


def hitung_similarity(item_a,item_b,list_irisan_a_b):
    atas=0
    bawah_kiri=0
    bawah_kanan=0
    l_atas=[]
    l_bawah_kiri=[]
    l_bawah_kanan=[]
    for user in list_irisan_a_b:

        atas+=data.at[user-1,item_a]*data.at[user-1,item_b]
        l_atas.append(data.at[user-1,item_a]*data.at[user-1,item_b])
        bawah_kiri+=data.at[user-1,item_a]**2
        l_bawah_kiri.append(data.at[user-1,item_a]**2)
        bawah_kanan += data.at[user - 1, item_b] ** 2
        l_bawah_kanan.append(data.at[user - 1, item_b] ** 2)
    bawah=(math.sqrt(bawah_kiri)) * (math.sqrt(bawah_kanan))
    hasil=atas / bawah
    print(l_atas)
    print(l_bawah_kiri)
    print(l_bawah_kanan)
    print(hasil)

    return hasil


for item_target in temp_item_kosong:
    for item_pembanding in temp_item_terisi:
        list_irisan_a_b=cari_user(item_target,item_pembanding)
        data_2.at[item_target,item_pembanding]=hitung_similarity(item_target,item_pembanding,list_irisan_a_b)


data_2.to_csv("matrix_similaritas_item.csv")