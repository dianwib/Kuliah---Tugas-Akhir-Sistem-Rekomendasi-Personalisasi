import pandas as pd
import numpy as np
import math

matrik_mae = pd.DataFrame(columns=['Item Hidden','MAE Traditional', 'MAE Userrank'])
def evaluasi_mae(fold=1):
    matrix_asli = pd.read_csv("matrik_rating.csv")
    matrix_asli.set_index('Unnamed: 0', inplace=True)
    def cari_data_hidden(user,matrix_asli,matrix_test):
        temp_item_data_test=[]
        for item in matrix_asli.columns:
            if not math.isnan(matrix_asli.at[user, item]) and matrix_asli.at[user, item] != matrix_test.at[user,item]:
                print(user,item)
                print(matrix_asli.at[user, item],matrix_test.at[user, item])
                temp_item_data_test.append(item)
        return temp_item_data_test

    def hitung_mae(user_target,list_data_test,matrix_asli,matrix_test):
        temp_nilai_atas=0
        for item in list_data_test:
            temp_nilai_atas+=math.fabs(matrix_asli.at[user_target,item] - matrix_test.at[user_target,item])
            print(matrix_asli.at[user, item],'-', matrix_test.at[user, item])
        hasil=float(temp_nilai_atas / len(list_data_test))

        return hasil

    for i in range (1,fold+1):
        data_test_traditional_itembase = pd.read_csv("test_"+str(i)+"_matrik_prediksi_traditional_itembase.csv")
        data_test_userrank_itembase = pd.read_csv("test_"+str(i)+"_matrik_prediksi_userrank_itembase.csv")
        data_test_userrank_itembase.set_index('Unnamed: 0', inplace=True)
        data_test_traditional_itembase.set_index('Unnamed: 0', inplace=True)

    eval_traditional=0.0
    eval_userrank = 0.0
    for user in matrix_asli.index:
        print(user)
        kumpulan_data_test=cari_data_hidden(user,matrix_asli,data_test_traditional_itembase)
        print(kumpulan_data_test)
        if len(kumpulan_data_test)==0:
            continue
        else:

            hasil_mae_traditional_itembase=hitung_mae(user,kumpulan_data_test,matrix_asli,data_test_traditional_itembase)
            hasil_mae_userrank_itembase=hitung_mae(user,kumpulan_data_test,matrix_asli,data_test_userrank_itembase)

        print("user >>",user,"\nMAE traditional :",hasil_mae_traditional_itembase,"\nMAE userrank :",hasil_mae_userrank_itembase)
        eval_traditional+=hasil_mae_traditional_itembase
        eval_userrank += hasil_mae_userrank_itembase

        matrik_mae.at[user, 'Item Hidden'] = kumpulan_data_test
        matrik_mae.at[user,'MAE Traditional']=eval_traditional
        matrik_mae.at[user, 'MAE Userrank'] = eval_userrank
    eval_userrank=eval_userrank/fold
    eval_traditional=eval_traditional/fold
    print(">>>>>>>>>>>>>>>\neval all\nTraditional :",eval_traditional,"\nUserrank :",eval_userrank)

evaluasi_mae(1)
print(matrik_mae)
