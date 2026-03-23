import pandas as pd

CLEAN_CSV = "extracted_data.csv"

def getCasesFromCSV(): 
    df = pd.read_csv(CLEAN_CSV)

    allCaseNames = []

    for row in df.iterrows(): 

        if row[1]["Case"] not in allCaseNames:
            allCaseNames.append(row[1]["Case"])
        
    allCaseNames = sorted(allCaseNames)
    return allCaseNames


def getFeaturesAsMatrix(): 
    df = pd.read_csv(CLEAN_CSV)
    examples = []

    WANTED_FEATURES = ["Weapon_ID", "Case_ID", "Rarity", "Wear_ID", "StatTrak"]
    
    for _, row in df.iterrows(): 
        curFeatures = []

        for col in WANTED_FEATURES:     
            curFeatures.append(row[col])
        
        examples.append(curFeatures)

    return examples

def getValuesAsArray(): 
    df = pd.read_csv(CLEAN_CSV)
    values = []

    for _, row in df.iterrows(): 
        values.append(row["Price"])
    
    return values


def getMAE(y_predicted, y_test): 
    total = 0

    for i in range(len(y_predicted)):
        total += abs(y_predicted[i] - y_test[i])
    
    total = total / len(y_predicted)
    return total

def getRMSE(y_predicted, y_test): 
    
    sds = 0
    for i in range(len(y_predicted)): 
        sds += (y_predicted[i] - y_test[i])**2
    
    sds = sds / len(y_predicted)
    sds = sds**0.5
    return sds


