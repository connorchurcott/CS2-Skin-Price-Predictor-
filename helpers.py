import pandas as pd
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.model_selection import cross_val_score, KFold
import numpy as np

CLEAN_CSV = "extracted_data.csv"


def getCasesFromCSV():
    df = pd.read_csv(CLEAN_CSV)

    allCaseNames = []

    for row in df.iterrows():

        if row[1]["Case"] not in allCaseNames:
            allCaseNames.append(row[1]["Case"])

    allCaseNames = sorted(allCaseNames)
    return allCaseNames


def convertUserInputToFeatures(weapon, case, rarity, wear, isStatTrak):
    df = pd.read_csv(CLEAN_CSV)

    allWeapons = df["Weapon"].unique()
    weaponEncode = {}
    for i, curWeapon in enumerate(allWeapons):
        weaponEncode[curWeapon] = i

    allCases = df["Case"].unique()
    caseEncode = {}
    for i, curCase in enumerate(allCases):
        caseEncode[curCase] = i

    wears = {
        "Factory New (FN)": 0,
        "Minimal Wear (MW)": 1,
        "Field-Tested (FT)": 2,
        "Well-Worn (WW)": 3,
        "Battle-Scared (BS)": 4,
    }

    rarities = {
        "Mil-Spec (Blue)": 1,
        "Restricted (Purple)": 2,
        "Classified (Pink)": 3,
        "Covert (Red)": 4,
        "Contraband (Yellow)": 5,
    }

    statTrak = {"Yes": 1, "No": 0}

    weaponID = weaponEncode[weapon]
    caseID = caseEncode[case]
    rarityID = rarities[rarity]
    wearID = wears[wear]
    statTrakID = statTrak[isStatTrak]

    return [weaponID, caseID, rarityID, wearID, statTrakID]


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
    y_predicted = np.array(y_predicted)
    y_test = np.array(y_test)

    total = np.mean(np.abs(y_predicted - y_test))
    return total


def getRMSE(y_predicted, y_test):
    y_predicted = np.array(y_predicted)
    y_test = np.array(y_test)

    mse = np.mean((y_predicted - y_test) ** 2)
    rmse = np.sqrt(mse)
    return rmse


def getMAPE(y_predicted, y_test):
    y_predicted = np.array(y_predicted, dtype=float)
    y_test = np.array(y_test, dtype=float)

    mask = np.abs(y_test) > 0.01

    if not np.any(mask):
        return 0.0

    y_test_filtered = y_test[mask]
    y_pred_filtered = y_predicted[mask]

    percentage_errors = np.abs((y_test_filtered - y_pred_filtered) / y_test_filtered)
    mape_decimal = np.mean(percentage_errors)

    mape_percentage = mape_decimal * 100

    return mape_percentage


def getcrossvalidation(x, y, split, model):

    folds = KFold(n_splits=split, shuffle=True)
    score = cross_val_score(model, x, y, cv=folds)
    return score.mean()
