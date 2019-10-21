import pandas as pd
import numpy as np

data=pd.read_csv("dataset.csv")
data_2=pd.DataFrame(data,index=np.arange(1,data["User ID"].max()+1),columns=np.array(1,data["Movie ID"].max()+1))
for i in range ((len(data.index))):
    user=data.at[i,"User ID"]
    film=data.at[i,"Movie ID"]
    rating=data.at[i,"Rating"]
    print("user >>",user,"  item >>",film,"  rating >>",rating)

    data_2.at[user,film]=rating

data_2.to_csv("matrix_rating.csv")
print(data.columns)
