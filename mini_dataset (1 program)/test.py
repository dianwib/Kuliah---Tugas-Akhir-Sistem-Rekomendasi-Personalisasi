import pandas as pd
import numpy as np
import math

class dataset():

    def __init__(self):
        self.matrix_dataset=pd.read_csv("test_dataset.csv")

    def matrix_rm(self):
        self.matrix_rm = pd.DataFrame(self.matrix_dataset, index=np.arange(1, self.matrix_dataset["User ID"].max() + 1),columns=np.array(1, self.matrix_dataset["Movie ID"].max() + 1))
        for i in range((len(self.matrix_dataset.index))):
            user = self.matrix_dataset.at[i, "User ID"]
            film = self.matrix_dataset.at[i, "Movie ID"]
            rating = self.matrix_dataset.at[i, "Rating"]
            self.matrix_rm.at[user, film] = rating

        #convert NaN to 0
        #for item in self.matrix_rm.columns:
        #    self.matrix_rm[item].fillna(0.0, inplace=True)
        return self.matrix_rm

    def matrix_crm(self,jml_user):
        self.matrix_crm = pd.DataFrame(index=np.arange(1,  jml_user + 1), columns=np.arange(1, jml_user + 1))
        for user in self.matrix_rm.index:
            for user_pembanding in self.matrix_rm.index:
                if user == user_pembanding:
                    self.matrix_crm.at[user, user_pembanding] = 0
                    continue
                temp = 0
                for item in self.matrix_rm.columns:
                    if self.matrix_rm.at[user, item] > 0 and self.matrix_rm.at[user_pembanding, item] > 0:
                        temp += 1
                self.matrix_crm.at[user, user_pembanding] = temp
        return self.matrix_crm

    def matrix_cm(self):
        self.matrix_cm = self.matrix_crm
        for user in self.matrix_crm.index:
            c = self.matrix_crm.sum(axis=1, skipna=True)
            for item in self.matrix_crm.columns:
                if self.matrix_crm.at[user, item] > 0:
                    data_lama = self.matrix_crm.at[user,item]
                    data_baru = data_lama / c[user]
                    self.matrix_cm.at[user, item] = data_baru
        return self.matrix_cm

    def pageRank(self,alpha=0.5,nilai_error=0.001):
        self.kolom_iterasi=0
        jml_user=len(self.matrix_rm.index)
        self.matrix_pageRank = pd.DataFrame(index=np.arange(1, jml_user + 1))
        self.matrix_pageRank[0] = 0.2

        def cek_selisih(kolom_iterasi, batas_error): #ecluidean distance
            temp_nilai = 0
            for user_rank in self.matrix_pageRank.index:
                temp_nilai += (self.matrix_pageRank.at[user_rank, kolom_iterasi + 1] - self.matrix_pageRank.at[
                    user_rank, kolom_iterasi])**2
            selisih_error = math.sqrt(temp_nilai)
            if selisih_error < batas_error:
                ketemu = True
            else:
                ketemu=False
                self.kolom_iterasi+=1
            return ketemu

        def list_uk(): #buat cari node tetangga user
            dict_list_uk = {}
            for user_n in (self.matrix_cm.index):
                temp = 0
                uk = []
                for user_k in (self.matrix_cm.columns):
                    if self.matrix_cm.at[user_n, user_k] > 0:
                        temp += 1
                        uk.append(user_k)
                dict_list_uk[user_n] = uk
            return dict_list_uk

        while True:
            for user in self.matrix_cm.index:
                temp = 0
                # print("UR User : ", user)
                for out_user in list_uk()[user]:
                    temp += self.matrix_pageRank.at[out_user, self.kolom_iterasi] * self.matrix_cm.at[out_user, user]
                    # print("data uk : ", self.matrix_pageRank.at[out_user, self.kolom_iterasi], "data cm : ", self.matrix_cm.at[out_user, user],
                    #        "hasil uk*cm : ", temp)
                hasil = ((1 - alpha ) * self.matrix_pageRank.at[user, self.kolom_iterasi]) + (alpha * temp)
                # print("data un : ", self.matrix_pageRank.at[user, self.kolom_iterasi], "hasil ur : ", hasil)
                self.matrix_pageRank.at[user, self.kolom_iterasi + 1] = hasil
            if cek_selisih(self.kolom_iterasi,nilai_error)==True:
                break

        return self.matrix_pageRank

    def matrix_s(self,jml_user,jml_item):

        matrix_temp_nilai_total_user = self.matrix_rm.sum(axis=1, skipna=True)
        matrix_temp_nilai_rata_user=matrix_temp_nilai_total_user
        for user in self.matrix_rm.index:
            list_total_user = []
            for item in self.matrix_rm.columns:
                if self.matrix_rm.at[user, item] > 0:
                    list_total_user.append(item)
            matrix_temp_nilai_rata_user[user] = float(matrix_temp_nilai_total_user[user] / len(list_total_user))
        #print(matrix_temp_nilai_rata_user)
        #print(self.matrix_rm)

        self.matrix_s=pd.DataFrame(index=np.arange(1,  jml_user + 1), columns=np.arange(1, jml_item + 1))
        for user in self.matrix_rm.index:
            #print(self.matrix_rm.loc[user],matrix_temp_nilai_rata_user[user])

            self.matrix_s.loc[user] = self.matrix_rm.loc[user]-matrix_temp_nilai_rata_user[user]

        return self.matrix_s

    def matrix_similarity_userrank(self,input_user=1):

        def cari_user(item_a, item_b):
            irisan_user_pada_item_a_b = []
            for user in self.matrix_s.index:
                if user != input_user:
                    if not math.isnan(self.matrix_s.at[user, item_a])  and not math.isnan(self.matrix_s.at[user, item_b]):
                        irisan_user_pada_item_a_b.append(user)
                else:
                    continue
            #print("user yang merating item ", item_a, item_b, ": user ", irisan_user_pada_item_a_b)
            return irisan_user_pada_item_a_b

        def hitung_similarity(item_a, item_b, list_irisan_a_b):
            atas = 0
            bawah_kiri = 0
            bawah_kanan = 0
            l_atas = []
            l_bawah_kiri = []
            l_bawah_kanan = []
            for user in list_irisan_a_b:
                kolom_terakhir = (self.matrix_pageRank.columns[-1])
                #print("pagerank user", user, "= ", self.matrix_pageRank.at[user, kolom_terakhir], "**2:",self.matrix_pageRank.at[user, kolom_terakhir] ** 2)

                atas += self.matrix_s.at[user, item_a] * self.matrix_s.at[user, item_b] * (self.matrix_pageRank.at[
                                                                                 user, kolom_terakhir] ** 2)  # str karena tipe data kolom pagerank adlh string
                l_atas.append(self.matrix_s.at[user, item_a] * self.matrix_s.at[user, item_b] * (self.matrix_pageRank.at[user, kolom_terakhir] ** 2))
                #print("similaritas ", user, item_a, ":", self.matrix_s.at[user, item_a], "dan", user, item_b, ":",self.matrix_s.at[user, item_b], "userrank", user, ":", (self.matrix_pageRank.at[user, kolom_terakhir] ** 2))

                bawah_kiri += (self.matrix_s.at[user, item_a] ** 2) * (self.matrix_pageRank.at[user, kolom_terakhir] ** 2)
                l_bawah_kiri.append((self.matrix_s.at[user, item_a] ** 2) * (self.matrix_pageRank.at[user, kolom_terakhir] ** 2))
                #print("similaritas ", user, item_a, ":", self.matrix_s.at[user, item_a] ** 2, "userrank", user, ":",self.matrix_pageRank.at[user, kolom_terakhir])

                bawah_kanan += (self.matrix_s.at[user, item_b] ** 2) * (self.matrix_pageRank.at[user, kolom_terakhir] ** 2)
                l_bawah_kanan.append((self.matrix_s.at[user, item_b] ** 2) * (self.matrix_pageRank.at[user, kolom_terakhir] ** 2))
                #print("similaritas ", user, item_b, ":", self.matrix_s.at[user, item_b] ** 2, "userrank", user, ":",                  self.matrix_pageRank.at[user, kolom_terakhir])

            bawah = (math.sqrt(bawah_kiri)) * (math.sqrt(bawah_kanan))
            hasil = float(atas / bawah)
            # print("sum atas ", l_atas)
            # print("sum bawah kiri ", l_bawah_kiri)
            # print("sum bawah kanan ", l_bawah_kanan)
            # print("atas ", atas)
            # print("bawah kiri ", math.sqrt(bawah_kiri))
            # print("bawah kanan ", math.sqrt(bawah_kanan))
            # print("bawah ", bawah)
            # print("similaritas ", item_a, item_b)
            # print("hasil", hasil, ">>>>>>>>>>>\n")
            return hasil

        data_similaritas_user = pd.DataFrame(dtype=float)

        temp_item_kosong = []
        temp_item_terisi = []
        #print(input_user)

        for item in (self.matrix_s.columns):
            if math.isnan(self.matrix_s.at[input_user, item]):
                temp_item_kosong.append(item)
            else:
                temp_item_terisi.append(item)

        for item_target in temp_item_kosong:
            for item_pembanding in temp_item_terisi:
                list_irisan_a_b = cari_user(item_target, item_pembanding)
                if len(list_irisan_a_b) == 0:
                    continue
                else:
                    data_similaritas_user.at[item_target, item_pembanding] = hitung_similarity(item_target, item_pembanding,list_irisan_a_b)
        print(data_similaritas_user)
        return data_similaritas_user


    def matrix_similarity_traditional(self,input_user=1):

        def cari_user(item_a, item_b):
            irisan_user_pada_item_a_b = []
            for user in self.matrix_s.index:
                if user != input_user:
                    if not math.isnan(self.matrix_s.at[user, item_a])  and not math.isnan(self.matrix_s.at[user, item_b]):
                        irisan_user_pada_item_a_b.append(user)
                else:
                    continue
            #print("user yang merating item ", item_a, item_b, ": user ", irisan_user_pada_item_a_b)
            return irisan_user_pada_item_a_b

        def hitung_similarity(item_a, item_b, list_irisan_a_b):
            atas = 0
            bawah_kiri = 0
            bawah_kanan = 0
            l_atas = []
            l_bawah_kiri = []
            l_bawah_kanan = []
            for user in list_irisan_a_b:
                atas += self.matrix_s.at[user, item_a] * self.matrix_s.at[user, item_b]
                l_atas.append(self.matrix_s.at[user, item_a] * self.matrix_s.at[user, item_b])
                bawah_kiri += self.matrix_s.at[user, item_a] ** 2
                l_bawah_kiri.append(self.matrix_s.at[user, item_a] ** 2)

                bawah_kanan += self.matrix_s.at[user, item_b] ** 2
                l_bawah_kanan.append(self.matrix_s.at[user, item_b] ** 2)
            bawah = (math.sqrt(bawah_kiri)) * (math.sqrt(bawah_kanan))

            hasil = float(atas / bawah)

            # print("sum atas ", l_atas)
            # print("sum bawah kiri ", l_bawah_kiri)
            # print("sum bawah kanan ", l_bawah_kanan)
            # print("atas ", atas)
            # print("bawah kiri ", math.sqrt(bawah_kiri))
            # print("bawah kanan ", math.sqrt(bawah_kanan))
            # print("bawah ", bawah)
            # print("similaritas ", item_a, item_b)
            # print("hasil", hasil, ">>>>>>>>>>>\n")
            return hasil

        data_similaritas_user = pd.DataFrame(dtype=float)

        temp_item_kosong = []
        temp_item_terisi = []
        #print(input_user)

        for item in (self.matrix_s.columns):
            if math.isnan(self.matrix_s.at[input_user, item]):
                temp_item_kosong.append(item)
            else:
                temp_item_terisi.append(item)

        for item_target in temp_item_kosong:
            for item_pembanding in temp_item_terisi:
                list_irisan_a_b = cari_user(item_target, item_pembanding)
                if len(list_irisan_a_b) == 0:
                    continue
                else:
                    data_similaritas_user.at[item_target, item_pembanding] = hitung_similarity(item_target, item_pembanding,list_irisan_a_b)
        print(data_similaritas_user)
        return data_similaritas_user

    def matrix_prediksi(self,tipe,input_K=2):

        def cari_tetangga(item_target, banyak_tetangga):
            temp_per_item_target = data.loc[item_target]  # select per index
            temp_per_item_target.sort_values(ascending=False, inplace=True)  # sorting desc
            temp_per_item_target = temp_per_item_target.iloc[:banyak_tetangga]  # spit berdasarkan max k
            #print(temp_per_item_target)
            list_QtU_item_k = temp_per_item_target.index.tolist()  # get index/item dari data stlh disorting convert ke list
            #print(list_QtU_item_k)
            return list_QtU_item_k

        def hitung_function(user_target, item_target, list_item_similar_qtu):
            atas = 0.0
            bawah = 0.0

            for item_similar in list_item_similar_qtu:
                atas += data.at[item_target, item_similar] * self.matrix_rm.at[user_target, item_similar]
                bawah += math.fabs(data.at[item_target, item_similar])
                #print("similaritas item(", item_target, item_similar, ")= ", data.at[item_target, item_similar]," * rating user item(", user_target, item_similar, ")= ",self.matrix_rm.at[user_target, item_similar])
                #print("absolute similaritas item(", item_target, item_similar, ")= ",math.fabs(data.at[item_target, item_similar]))
            hasil = float(atas) / float(bawah)
            #print(hasil)
            return hasil

        if tipe=="traditional":
            self.matrix_rm_plus_prediksi=self.matrix_rm.copy()
            for user_target in self.matrix_rm.index:
                data = self.matrix_similarity_traditional(user_target)
                data_hasil = {}
                for item_target in data.index:
                    QtU = cari_tetangga(item_target, input_K)
                    hasil = hitung_function(user_target, item_target, QtU)
                    data_hasil[item_target] = hasil
                    self.matrix_rm_plus_prediksi.at[user_target, item_target] = hasil

            return self.matrix_rm_plus_prediksi

        elif tipe == "userrank":
            self.matrix_rm_plus_prediksi_userrank = self.matrix_rm.copy()
            for user_target in self.matrix_rm.index:
                data = self.matrix_similarity_userrank(user_target)
                data_hasil = {}
                for item_target in data.index:
                    QtU = cari_tetangga(item_target, input_K)
                    hasil = hitung_function(user_target, item_target, QtU)
                    data_hasil[item_target] = hasil
                    self.matrix_rm_plus_prediksi_userrank.at[user_target, item_target] = hasil

            return self.matrix_rm_plus_prediksi_userrank

    def lihat_top_n(self,tipe="traditional",user_target=1,top_n=2):

        if tipe=="traditional":
            data_top_n = self.matrix_rm_plus_prediksi.loc[user_target]
            for item in self.matrix_rm.columns:
                if not math.isnan(self.matrix_rm.at[user_target, item]):
                    del data_top_n[item]

            data_top_n.sort_values(ascending=False, inplace=True)  # sorting desc
            data_top_n = data_top_n.iloc[:top_n]
            return (data_top_n)


        elif tipe == "userrank":
            data_top_n = self.matrix_rm_plus_prediksi_userrank.loc[user_target]
            for item in self.matrix_rm.columns:
                if not math.isnan(self.matrix_rm.at[user_target, item]):
                    del data_top_n[item]

            data_top_n.sort_values(ascending=False, inplace=True)  # sorting desc
            data_top_n = data_top_n.iloc[:top_n]
            return (data_top_n)

            #for item in self.matrix_rm.columns:





afni=dataset()
print(afni.matrix_dataset)
print(afni.matrix_rm())
total_user=len(afni.matrix_rm.index)
total_item=len(afni.matrix_rm.columns)
(afni.matrix_crm(total_user))
(afni.matrix_cm())
(afni.pageRank(nilai_error=0.00000001))
print(afni.matrix_rm)
# afni.matrix_rm.to_csv("matrik_rating.csv")

(afni.matrix_s(total_user,total_item))
print(">>>>>>>>>>>>>>>>>>>")
(afni.matrix_prediksi("traditional",2))

(afni.matrix_prediksi("userrank",2))
print(afni.matrix_rm_plus_prediksi)
afni.matrix_rm_plus_prediksi.to_csv("test_1_matrik_prediksi_traditional_itembase.csv")
print(afni.lihat_top_n("traditional",5,2))
print(afni.matrix_rm_plus_prediksi_userrank)
afni.matrix_rm_plus_prediksi_userrank.to_csv("test_1_matrik_prediksi_userrank_itembase.csv")
print(afni.lihat_top_n("userrank",5,2))