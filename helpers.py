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
