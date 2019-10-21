import pandas as pd
import numpy as np

data_2=pd.read_csv("matrix_rating.csv")

for i in data_2.columns:
    data_2[i].fillna(0.0,inplace=True)



data_2.to_csv("matrix_rating_fix.csv")

