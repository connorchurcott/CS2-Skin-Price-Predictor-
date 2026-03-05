import numpy as np
import pandas as pd

DATA = "Skins_Price.csv"

df = pd.read_csv(DATA)

print(df.keys())