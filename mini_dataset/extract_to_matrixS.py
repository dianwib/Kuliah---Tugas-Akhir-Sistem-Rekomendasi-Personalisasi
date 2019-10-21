import pandas as pd

data=pd.read_csv("matrix_rm.csv", dtype=float)
del data['Unnamed: 0']
print(len (data.index))
data.index=pd.RangeIndex(start=1, stop=len(data.index)+1,step=1)

print(data)
data_2=data
for user in data.index:
    #print(user)
    temp_nilai_total_user=0
    list_total_user=[]
    for item in data.columns:
        if data.at[user,item]>0:
            list_total_user.append(item)
            temp_nilai_total_user+=data.at[user,item]

    nilai_rata_user=float (temp_nilai_total_user / len(list_total_user))
    print(user,"user",temp_nilai_total_user ,"total" ,len(list_total_user),"jml","=",nilai_rata_user)
    for item in data.columns:
        #jika matrix index nilai 0
        if data.at[user,item] == 0.0:
            print(user,item," ==0")
            data_2.at[user, item] = 0.0;
        else:
            nilai_matrix_lama=float(data.at[user,item])
            print(user,item)
            print(nilai_matrix_lama,"mat lama ","baru =",float(nilai_matrix_lama- nilai_rata_user))
            data_2.at[user,item]=float(nilai_matrix_lama- nilai_rata_user)



data_2.to_csv("matrix_s.csv")