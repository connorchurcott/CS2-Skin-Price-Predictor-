import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

DATA = "Skins_Price.csv"

#Some values of the prices are labelled as Not Possible
df = pd.read_csv(DATA)


def get_price(price):
    #Returns a new dataframe with the chosen price.
    #Price is divided between Factory New, Minimal Wear, Field-Tested, Well-Worn, Battle-Scarred
    #And their StatTrak versions
    final = df[['Weapon','Case','Rarity','Min Wear','Max Wear','Case_1',price]].copy(deep=True) 
    return final

def replace_rarity(rarity):
    #Rarity order: [Mil-spec, Restricted, Classified, Covert, Contraband]

    #extract the rarity
    rarities = rarity.str.split().str[0]
    #replaces the rarities with their corresponding values
    final = rarities.replace({'Mil-Spec': 1, 'Restricted': 2, 'Classified': 3, 'Covert': 4, 'Contraband': 5})

    return final

#replace the rarity column with numeric values
df['Rarity'] = replace_rarity(df['Rarity'])
