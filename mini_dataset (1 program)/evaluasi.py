import pandas as pd
import numpy as np
import math

fold_matrik_mae = pd.DataFrame(columns=['Fold', 'MAE Traditional', 'MAE Userrank'])


class evaluasi():
    def __init__(self,nama_dataset):
        self.hidden_dataset=pd.read_csv(nama_dataset)
        print(self.hidden_dataset)
        self.matrix_rm_hidden()

    def matrix_rm_hidden(self):
        self.matrix_rm_hidden = pd.DataFrame( dtype=float)
        for i in range((len(self.hidden_dataset.index))):
            user = self.hidden_dataset.at[i, "User ID"]
            film = self.hidden_dataset.at[i, "Movie ID"]
            rating = self.hidden_dataset.at[i, "Rating"]
            self.matrix_rm_hidden.at[user, film] = rating

        print(self.matrix_rm_hidden,"hidden")
        return self.matrix_rm_hidden


    def evaluasi_mae(self,fold):
        self.matrix_prediksi_traditional_itembase = pd.read_csv("base_" + str(fold) + "_matrik_prediksi_traditional_itembase.csv")
        self.matrix_prediksi_userrank_itembase = pd.read_csv("base_" + str(fold) + "_matrik_prediksi_userrank_itembase.csv")
        self.matrix_prediksi_userrank_itembase.set_index('Unnamed: 0', inplace=True)
        self.matrix_prediksi_traditional_itembase.set_index('Unnamed: 0', inplace=True)

        def cari_data_hidden(user):
            temp_item_data_test = []
            for item in self.matrix_rm_hidden.columns:
                if not math.isnan(self.matrix_rm_hidden.at[user, item]):
                    temp_item_data_test.append(item)
            return temp_item_data_test

        def hitung_mae(user_target, list_data_test, matrix_test):
            temp_nilai_atas = 0
           # print(matrix_test,"matrix prediksi")
            for item in list_data_test:#menghitung nilai mae pada setiap user (seluruh item)
                print("data hidden - data prediksi || user target" ,user_target,"item",item,self.matrix_rm_hidden.at[user_target, item], '-', matrix_test.at[user_target, str(item)])
                temp_nilai_atas += math.fabs(self.matrix_rm_hidden.at[user_target, item] - matrix_test.at[user_target, str(item)])

            hasil = float(temp_nilai_atas)
            print("user",user_target,"hasil",hasil)
            return hasil

        eval_traditional = 0.0
        eval_userrank = 0.0
        for user in self.matrix_rm_hidden.index :
            print("<<< user >>> ",user)
            kumpulan_data_test = cari_data_hidden(user)
            print("user target di data hidden: ", user," dan item hidden: ",kumpulan_data_test)
            print("\ntraditional")

            hasil_mae_traditional_itembase = hitung_mae(user, kumpulan_data_test,
                                                            self.matrix_prediksi_traditional_itembase)
            print("\nuserrank+traditional")
            hasil_mae_userrank_itembase = hitung_mae(user, kumpulan_data_test,
                                                         self.matrix_prediksi_userrank_itembase)
            # #
            # # # set to local pd
            # # matrik_mae.at[user, 'Item Hidden'] = kumpulan_data_test
            # # matrik_mae.at[user, 'MAE Traditional'] = hasil_mae_traditional_itembase
            # # matrik_mae.at[user, 'MAE Userrank'] = hasil_mae_userrank_itembase
            #
            # print("user >>", user, "\nMAE traditional :", hasil_mae_traditional_itembase, "\nMAE userrank :",
            #       hasil_mae_userrank_itembase)

            eval_traditional += hasil_mae_traditional_itembase #nilai mae tiap user update (+) dr seluruh user
            eval_userrank += hasil_mae_userrank_itembase



        mae_total_eval_userrank = eval_userrank / len(self.hidden_dataset.index) #nilai total mae dibagi banyak data hidden
        mae_total_eval_traditional = eval_traditional / len(self.hidden_dataset.index)

        print(">>>>>>>>>>>>>>>\neval all fold ke ",fold,"\nTraditional :", mae_total_eval_traditional, "\nUserrank :", mae_total_eval_userrank)

        fold_matrik_mae.at[fold, "Fold"] = fold
        fold_matrik_mae.at[fold, 'MAE Userrank'] = mae_total_eval_userrank
        fold_matrik_mae.at[fold, 'MAE Traditional'] = mae_total_eval_traditional


total_fold=5
for fold in range(1,total_fold+1):
    afni = evaluasi("hidden_base_" + str(fold) + "_dataset.csv")
    afni.evaluasi_mae(fold)


temp_mae_traditional=0.0
temp_mae_userrank=0.0
for fold in fold_matrik_mae.index:
    temp_mae_traditional+=fold_matrik_mae.at[fold,'MAE Traditional']
    temp_mae_userrank += fold_matrik_mae.at[fold, 'MAE Userrank']
print(">>>>>>>>>>>>>>>")
print(fold_matrik_mae)
print(">>>>>>>>>>>>>>>\nHasil akhir ",total_fold, " fold\nMAE Traditional :", temp_mae_traditional/total_fold, "\nMAE Traditional + Userrank :",
      temp_mae_userrank/total_fold)

