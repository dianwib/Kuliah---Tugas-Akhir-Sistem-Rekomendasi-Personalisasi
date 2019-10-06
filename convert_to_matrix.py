import pandas as pd
import numpy as np

data=pd.read_csv("dataset_1.csv")
data_2=pd.DataFrame(data,index=np.array(1-944),columns=np.array(1-1683))
a=(len(data.index))

for i in range (a):
    user=data.at[i,"UserID"]
    film=data.at[i,"ItemID"]
    rating=data.at[i,"Rating"]
    print("user >>",user,"  item >>",film,"  rating >>",rating)

    data_2.at[user,film]=rating

data_2.to_csv("rating.csv")
print(data.columns)
