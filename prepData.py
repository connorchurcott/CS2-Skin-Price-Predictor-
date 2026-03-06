import pandas as pd

def convertColsIntoRows():
    # changes each row price into its own column so we can pass it to the model easier

    normWears = {
        "Factory New": "FN",
        "Minimal Wear": "MW",
        "Field-Tested": "FT",
        "Well-Worn": "WW",
        "Battle-Scarred": "BS"
    }

    stWears = {
        "StatTrak Factory New": "FN",
        "StatTrak Minimal Wear": "MW",
        "StatTrak Field-Tested": "FT",
        "StatTrak Well-Worn": "WW",
        "StatTrak Battle-Scarred": "BS"
    }
    
    dataFrame = pd.read_csv("Skins_Price.csv")
    newRows = []

    for _, row in dataFrame.iterrows(): 

        # non-stattrak skins 
        for col, wear in normWears.items():
            price = row[col]

            if price == "Not Possible" or price == "No Recent Price": 
                continue
            else:
                price = float(str(price).replace('$',"").replace(',', ""))

            newRows.append({
                "weapon": row["Weapon"], 
                "rarity": row["Rarity"], 
                "case": row["Case"], 
                "wear": wear, 
                "isStatTrak": 0, 
                "price": price
            })

        #stattrak skins
        for col, wear in stWears.items(): 
            price = row[col]

            if price == "Not Possible" or price == "No Recent Price": 
                continue 
            else: 
                price = float(str(price).replace('$', "").replace(',', ""))

            newRows.append({
                "weapon": row["Weapon"], 
                "rarity": row["Rarity"], 
                "case": row["Case"], 
                "wear": wear, 
                "isStatTrak": 1, 
                "price": price
            })

    newDataFrame = pd.DataFrame(newRows)
    return newDataFrame


def trimRaritySection(dataFrame: pd.DataFrame): 
    # gets rid of the wepon type from the rarity col
    
    for i, row in dataFrame.iterrows(): 
        rarity = row["rarity"]
        rarity = str(rarity).split(" ")[0]
        dataFrame.loc[i, "rarity"] = rarity
    

def createCleanedDataFrame(): 
    dataFrame = convertColsIntoRows()
    trimRaritySection(dataFrame)
    return dataFrame

df = createCleanedDataFrame()
print(df.head(20))

